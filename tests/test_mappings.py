import gab_tidy_data.gab_data_mapping as data_mapping
from importlib.resources import open_text


def test_mapping_completeness():
    # There is insert_sql for all tables
    assert set(data_mapping.insert_sql.keys()) == set(data_mapping.data_table_names)


def test_schema_version_match():
    # Find schema version in SQL file
    with open_text("gab_tidy_data", "gab_schema.sql") as sql_fh:
        for line in sql_fh.readlines():
            if "schema_version" in line:
                break

        assert "schema_version" in line

    # Relies on double quotes being used around the strings. Is there a better way?
    sql_version = line.rsplit('"')[-2]

    # Does the SQL version match the version in the mapping file?
    assert sql_version == data_mapping.schema_version
