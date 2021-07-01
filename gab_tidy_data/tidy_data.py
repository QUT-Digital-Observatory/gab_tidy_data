from logging import getLogger
import sqlite3
import json
from os import path

from typing import Tuple


logger = getLogger(__name__)


def initialise_empty_database(db_connection: sqlite3.Connection):
    sql_filename = "gab_schema.sql"

    with open(sql_filename, 'r') as sql_file:
        db_connection.executescript("\n".join(sql_file))

    db = db_connection.cursor()
    db.execute(".tables")
    created_tables = db.fetchall()
    logger.debug("Created database tables: " + str(created_tables))
    assert len(created_tables) == 8
    logger.info("The database schema has been initialised")


def parse_and_load_to_sqlite(json_files, db_filename) -> Tuple[int, int]:
    """
    Initialise database even if no files are given

    """
    db_is_new = True if not path.exists(db_filename) else False

    db_connection = sqlite3.connect(db_filename)

    if db_is_new:
        logger.debug("New database created")
        initialise_empty_database(db_connection)
        initial_gab_count = 0
    else:
        logger.debug("Connected to existing database")
        # How many gabs in the database already?
        db = db_connection.cursor()
        db.execute("select count(*) from gab")
        initial_gab_count = db.fetchone()[0]
        logger.debug(f"Database already has {initial_gab_count} gabs")
        
    gabs_at_end = 0

    return 0, gabs_at_end - initial_gab_count
