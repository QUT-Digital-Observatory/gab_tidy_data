import pytest
import sqlite3
from logging import getLogger
import gab_tidy_data.gab_to_sqlite as gts
import gab_tidy_data.gab_data_mapping as data_mapping


logger = getLogger(__name__)


@pytest.fixture
def new_database_conn(tmp_path):
    db_path = tmp_path / "init_empty.db"
    assert not db_path.exists()

    with sqlite3.connect(db_path) as connection:
        yield connection


def test_init_empty_db(new_database_conn):
    gts.initialise_empty_database(new_database_conn)

    db = new_database_conn.cursor()
    # ".tables" only works in the sqlite shell!
    db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    created_tables = db.fetchall()
    logger.debug("Created database tables: " + str(created_tables))
    assert len(created_tables) == len(gts.all_table_names)
    logger.info("The database schema has been initialised")


def test_version_check(new_database_conn, monkeypatch):
    gts.initialise_empty_database(new_database_conn)

    assert gts.schema_is_current(new_database_conn)

    monkeypatch.setattr(data_mapping, "schema_version", "fake_version")

    assert not gts.schema_is_current(new_database_conn)
