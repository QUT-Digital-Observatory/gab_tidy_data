import pytest
from click.testing import CliRunner
from gab_tidy_data.__main__ import gab_tidy_data as cli_main
from pathlib import Path
import sqlite3


# Sample json files
sample_data_directory = Path(__file__).parent.resolve() / "sample_data"

sample_data = [
    {"path": sample_data_directory / "sample01.json", "num_authors": 2, "num_posts": 2},
    {"path": sample_data_directory / "sample02.json", "num_authors": 2, "num_posts": 2},
    {"path": sample_data_directory / "sample03.json", "num_authors": 1, "num_posts": 1},
]


@pytest.mark.parametrize(
    "samples_to_use", [([]), ([sample_data[0]]), (sample_data[0:3])]
)
def test_cli(tmp_path, samples_to_use):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        for s in samples_to_use:
            # Ensures the test files are set up right before running
            assert s["path"].exists()

        data_path_strings = [str(s["path"]) for s in samples_to_use]
        db_path = tmp_path / "cli_test.db"

        args = data_path_strings + [str(db_path)]
        result = runner.invoke(cli_main, args)
        assert result.exit_code == 0

        # Did it create the database?
        assert db_path.exists()

        # Is there the right amount of data in key tables?
        with sqlite3.connect(db_path) as db_connection:
            db = db_connection.cursor()

            db.execute("select count(*) from account")
            expected_authors = sum([s["num_authors"] for s in samples_to_use])
            assert db.fetchone()[0] == expected_authors

            db.execute("select count(*) from gab")
            expected_posts = sum([s["num_posts"] for s in samples_to_use])
            assert db.fetchone()[0] == expected_posts
