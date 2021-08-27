import pytest
from click.testing import CliRunner
from gab_tidy_data.__main__ import gab_tidy_data as cli_main
from pathlib import Path


# Sample json files
# Assumes tests are being run either from tests folder or repository base
if Path.cwd().name == "tests":
    sample_data_directory = Path("sample_data")
else:
    sample_data_directory = Path("tests", "sample_data")

sample_json = list(map(lambda p: p.resolve(), sample_data_directory.glob("*.json")))
assert len(sample_json) > 2


def test_cli(tmp_path):
    runner = CliRunner()

    # with runner.isolated_filesystem(temp_dir=tmp_path):
    # Test with no json files
    result = runner.invoke(cli_main, [str(tmp_path / "cli_test_0.db")])
    assert result.exit_code == 0
    assert (tmp_path / "cli_test_0.db").exists()

    # One json file
    assert sample_json[0].exists()
    result = runner.invoke(cli_main, [str(sample_json[0]), str(tmp_path / "cli_test_1.db")])
    assert result.exit_code == 0
    assert (tmp_path / "cli_test_1.db").exists()

    # Multiple json files
    result = runner.invoke(cli_main, [str(sample_json[0]), str(sample_json[1]), str(tmp_path / "cli_test_2.db")])
    assert result.exit_code == 0
    assert (tmp_path / "cli_test_2.db").exists()