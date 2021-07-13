from logging import getLogger
import sqlite3
import json
from pathlib import Path
from click import format_filename

from typing import Tuple, TextIO, Sequence

from gab_data_mapping import *


logger = getLogger(__name__)

metadata_table_names = [
    '_gab_tidy_data',
    '_inserted_files'
]
all_table_names = metadata_table_names + data_table_names


def initialise_empty_database(db_connection: sqlite3.Connection):
    sql_filename = "gab_schema.sql"
    # TODO: assumes working directory :( :( :(
    sql_filepath = Path("gab_tidy_data") / sql_filename
    logger.debug(f"Initialising database from {str(sql_filepath)}")

    with sql_filepath.open() as sql_file:
        db_connection.executescript("\n".join(sql_file))

    db_connection.commit()

    db = db_connection.cursor()  # todo: inconsistent with other db uses
    # ".tables" only works in the sqlite shell!
    db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    created_tables = db.fetchall()
    logger.debug("Created database tables: " + str(created_tables))
    assert len(created_tables) == len(all_table_names)
    logger.info("The database schema has been initialised")
    db.close()


def validate_existing_database(db_connection: sqlite3.Connection):
    """
    Does not validate schema or state of database in detail, just checks suitability
    for use - namely, that the schema version matches.
    """
    # todo: handle case if db file exists but no tables exist
    # todo: handle schema version
    pass


# todo: what would be useful to return???
def load_file_to_sqlite(json_fh: TextIO, db_connection):
    """
    Parse and load Garc output json file into database using data mappings

    Garc output is one json object per line. No [] wrapping the whole, no comma between
    objects.

    Note: the "fh" in "json_fh" is short for "file handler"
    """
    db = db_connection.cursor()
    # Filename string to use for logging, output, metadata etc
    friendly_filename = format_filename(json_fh.name, shorten=True)

    failed_parsing = []

    # File metadata
    db.execute("""
        insert into _inserted_files (filename, inserted_by_version)
        values (:filename, :inserted_by_version)
    """, {"filename": friendly_filename, "inserted_by_version": "superalpha"}
    )

    file_id = db.lastrowid

    for gab_line in json_fh:
        try:
            gab_json = json.loads(gab_line)
        except json.JSONDecodeError:
            failed_parsing.append(gab_line)
            continue  # Skip lines with JSON parsing issues

        # Parse this gab, and any gabs embedded within this gab
        gab_mappings = map_gab_for_insert(file_id, gab_json)

        for table, mappings in gab_mappings.items():
            if len(mappings) == 0 or len(mappings[0]) == 0: # such a hack - why is group coming up as [[]]?
                continue
            elif not isinstance(mappings, list):
                db.execute(insert_sql[table], mappings)
            else:
                db.executemany(insert_sql[table], mappings)

    # How many gabs were successfully inserted from this file
    db.execute("select count(*) from gab where _file_id = ?", [file_id])
    num_gabs_inserted = db.fetchone()[0]

    # Update the file metadata table accordingly
    db.execute("""
        update _inserted_files 
        set num_gabs_inserted = :num_gabs_inserted,
            num_parsing_failures = :num_parsing_failures
        where id = :file_id
    """, {"file_id": file_id, "num_gabs_inserted": num_gabs_inserted, "num_parsing_failures": len(failed_parsing)})

    # Done with this file!
    db_connection.commit()

    # todo better error message
    if len(failed_parsing) > 0:
        logger.warning(f"Failed to parse {len(failed_parsing)} lines of filename. These lines have been skipped.")

    logger.info(
        f"Finished loading file {friendly_filename}: {num_gabs_inserted} gabs "
        f"sucessfully added; {len(failed_parsing)} gabs skipped due to parsing "
        f"errors"
    )

