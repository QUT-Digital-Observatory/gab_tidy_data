import pytest
import sqlite3
from pathlib import Path
from logging import getLogger
from gab_tidy_data.gab_to_sqlite import all_table_names


logger = getLogger(__name__)


# There will be a problem if this is used more than 10 times
clean_db_count = range(0, 10)


@pytest.fixture
def new_database_connection(tmp_path):
    db_path = tmp_path / f"clean_{next(clean_db_count)}.db"
    assert not db_path.exists()

    with sqlite3.connect(db_path) as connection:
        yield connection


def test_init_empty_db(new_database_connection):
    db = new_database_connection.cursor()
    # ".tables" only works in the sqlite shell!
    db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    created_tables = db.fetchall()
    logger.debug("Created database tables: " + str(created_tables))
    assert len(created_tables) == len(all_table_names)
    logger.info("The database schema has been initialised")
