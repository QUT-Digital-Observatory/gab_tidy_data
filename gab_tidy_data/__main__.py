import click
import logging
import sqlite3
from os import path

from gab_to_sqlite import initialise_empty_database, validate_existing_database, load_file_to_sqlite

logging.basicConfig(filename="gab_tidy_data.log", level=logging.INFO)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('json_files', type=click.File('r'), nargs=-1)
@click.argument('database_filename', type=click.Path(dir_okay=False, writable=True), required=True)
@click.option('--log_level', type=click.Choice(["warning", "info", "debug"], case_sensitive=False))
def gab_tidy_data(json_files, database_filename, log_level):
    if log_level == "warning":
        logger.setLevel(logging.WARNING)
    elif log_level == "debug":
        logger.setLevel(logging.DEBUG)
        logger.debug("debug logging mode")

    logger.info(f"Loading {len(json_files)} JSON files into {database_filename}")
    click.echo(f"Loading {len(json_files)} JSON files into {database_filename}")

    db_is_new = True if not path.exists(database_filename) else False

    with sqlite3.connect(database_filename) as db_connection:
        # Check for database and initialise if needed
        if db_is_new:
            logger.debug("New database created")
            initialise_empty_database(db_connection)
        else:
            logger.debug("Connected to existing database")
            validate_existing_database(database_filename)

        for json_file in json_files:
            load_file_to_sqlite(json_file, db_connection)

    # click.echo(f"Successfully parsed {files_successful} JSON files, resulting in {num_gab_rows} gabs in database {database_filename}")


if __name__ == '__main__':
    gab_tidy_data()
