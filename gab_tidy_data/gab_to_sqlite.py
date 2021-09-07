from logging import getLogger
import sqlite3
import json
from click import format_filename

from typing import TextIO, Optional, Tuple
from importlib.resources import open_text
import datetime as dt

import gab_tidy_data.gab_data_mapping as data_mapping


logger = getLogger(__name__)

metadata_table_names = ["_gab_tidy_data", "_inserted_files"]
all_table_names = metadata_table_names + data_mapping.data_table_names


def initialise_empty_database(db_connection: sqlite3.Connection):
    with open_text("gab_tidy_data", "gab_schema.sql") as sql_file:
        logger.debug(f"Initialising database from SQL file {sql_file.name}")
        db_connection.executescript("\n".join(sql_file))

    db_connection.commit()


def load_file_to_sqlite(json_fh: TextIO, db_connection) -> Tuple[int, int]:
    """
    Parse and load Garc output json file into database using data mappings

    Garc output is one json object per line. No [] wrapping the whole, no comma between
    objects.

    Note: the "fh" in "json_fh" is short for "file handler"

    Returns (number of gabs inserted, number of posts which failed to parse). The total
    number of posts may be greater than the number of lines in the json file, as
    embedded gabs are also counted.
    """
    db = db_connection.cursor()
    # Filename string to use for logging, output, metadata etc
    friendly_filename = format_filename(json_fh.name, shorten=True)

    failed_parsing = []

    # File metadata
    db.execute(
        """
        insert into _inserted_files (filename, inserted_by_version)
        values (:filename, :inserted_by_version)
    """,
        {"filename": friendly_filename, "inserted_by_version": "superalpha"},
    )

    file_id = db.lastrowid

    for gab_line in json_fh:
        try:
            gab_json = json.loads(gab_line)
        except json.JSONDecodeError as e:
            failed_parsing.append(gab_line)
            logger.debug(exc_info=e, msg="Failed to parse input line. Skipping line.")
            continue  # Skip lines with JSON parsing issues

        # Parse this gab, and any gabs embedded within this gab
        gab_mappings = data_mapping.map_gab_for_insert(file_id, gab_json)

        for table, mappings in gab_mappings.items():
            if len(mappings) == 0 or len(mappings[0]) == 0:
                # such a hack - why is group coming up as [[]]?
                continue
            elif not isinstance(mappings, list):
                db.execute(data_mapping.insert_sql[table], mappings)
            else:
                db.executemany(data_mapping.insert_sql[table], mappings)

    # How many gabs were successfully inserted from this file
    db.execute("select count(*) from gab where _file_id = ?", [file_id])
    num_gabs_inserted = db.fetchone()[0]

    # Update the file metadata table accordingly
    db.execute(
        """
        update _inserted_files
        set num_gabs_inserted = :num_gabs_inserted,
            num_parsing_failures = :num_parsing_failures,
            inserted_at = :now
        where id = :file_id
    """,
        {
            "file_id": file_id,
            "num_gabs_inserted": num_gabs_inserted,
            "num_parsing_failures": len(failed_parsing),
            "now": dt.datetime.utcnow(),
        },
    )

    # Done with this file!
    db_connection.commit()

    if len(failed_parsing) > 0:
        logger.warning(
            f"Failed to parse {len(failed_parsing)} lines of filename. These lines have"
            f" been skipped. See debug logs for error information."
        )

    logger.info(
        f"Finished loading file {friendly_filename}: {num_gabs_inserted} gabs "
        f"successfully added; {len(failed_parsing)} gabs skipped due to parsing "
        f"errors"
    )

    return num_gabs_inserted, len(failed_parsing)


def fetch_db_contents(db_connection, since: Optional[dt.datetime] = None):
    """
    Gets the file insertion metadata from the database, including numbers of posts
    entered by each file. Can optionally add a since date to only return files at or
    after that time. All times are in UTC.

    Returns a list of inserted files: (filename, number of posts inserted, number of
    posts which failed to parse)
    """
    db = db_connection.cursor()

    date_clause = "where inserted_at >= julianday(:since)" if since else ""

    db.execute(
        """
            select filename, num_gabs_inserted, num_parsing_failures
            from _inserted_files
        """
        + date_clause,
        {"since": since},
    )

    return db.fetchall()


def schema_is_current(db_connection: sqlite3.Connection) -> bool:
    """
    Given an existing database, checks to see whether the schema version in the existing
    database matches the schema version for this version of Gab Tidy Data.
    """
    db = db_connection.cursor()

    db.execute(
        """
        select metadata_value from _gab_tidy_data
        where metadata_key = 'schema_version'
        """
    )

    db_schema_version = db.fetchone()[0]

    return db_schema_version == data_mapping.schema_version
