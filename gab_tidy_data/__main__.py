import click
import logging
import sqlite3
from os import path
import datetime as dt

import gab_tidy_data.gab_to_sqlite as gts

logging.basicConfig(filename="gab_tidy_data.log", level=logging.INFO)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("json_files", type=click.File("r"), nargs=-1)
@click.argument(
    "database_filename", type=click.Path(dir_okay=False, writable=True), required=True
)
@click.option(
    "--log_level", type=click.Choice(["warning", "info", "debug"], case_sensitive=False)
)
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
            gts.initialise_empty_database(db_connection)
        else:
            logger.debug("Connected to existing database")
            if not gts.schema_is_current(db_connection):
                # Sometimes the error message comes before the "Loading" echo statement
                # above and it's confusing to read. The following echo should confirm to
                # the user that their files weren't loaded.
                click.echo("Files not loaded.")
                raise click.ClickException(
                    f"Database {database_filename} already exists, and uses a database "
                    "schema that is a different version from the schema in the version "
                    "of Gab Tidy Data you are currently using. You will need to reload"
                    "your data (including any files previously loaded into "
                    f"{database_filename}) into a new database file."
                )

        time_started = dt.datetime.utcnow()

        for json_file in json_files:
            added, fails = gts.load_file_to_sqlite(json_file, db_connection)

            click.echo(
                f"- {json_file.name} loaded: {added} posts added; {fails} failed to add"
            )

        files_added = gts.fetch_db_contents(db_connection, time_started)

    total_posts_added = sum([n for _, n, _ in files_added])
    total_parse_fails = sum([n for _, _, n in files_added])

    click.echo(
        f"Parsed {len(files_added)} JSON files, resulting in {total_posts_added} posts "
        f"added to database {database_filename}. {total_parse_fails} posts failed to "
        "parse."
    )


if __name__ == "__main__":
    gab_tidy_data()
