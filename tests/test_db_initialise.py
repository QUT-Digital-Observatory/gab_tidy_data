import pytest
import sqlite3
from logging import getLogger
from gab_tidy_data.gab_to_sqlite import all_table_names, initialise_empty_database


logger = getLogger(__name__)


def test_init_empty_db(tmp_path):
    db_path = tmp_path / "init_empty.db"
    assert not db_path.exists()

    with sqlite3.connect(db_path) as connection:
        initialise_empty_database(connection)

        db = connection.cursor()
        # ".tables" only works in the sqlite shell!
        db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        created_tables = db.fetchall()
        logger.debug("Created database tables: " + str(created_tables))
        assert len(created_tables) == len(all_table_names)
        logger.info("The database schema has been initialised")
