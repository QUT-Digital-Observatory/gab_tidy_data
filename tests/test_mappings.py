import pytest
from gab_tidy_data import gab_data_mapping


def test_mapping_completeness():
    # There is insert_sql for all tables
    assert set(gab_data_mapping.insert_sql.keys()) == set(gab_data_mapping.data_table_names)

