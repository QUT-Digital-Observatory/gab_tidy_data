import click
import logging

from tidy_data import parse_and_load_to_sqlite

logging.basicConfig(filename="gab_tidy_data.log", level=logging.INFO)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('json_files', type=click.File('r'), nargs=-1)
@click.argument('database_filename', type=click.Path(dir_okay=False, writable=True), required=True)
@click.option('--log_level', type=click.Choice(["warning", "info", "debug"], case_sensitive=False))
def tidy_data(json_files, database_filename, log_level):
    if log_level == "warning":
        logger.setLevel(logging.WARNING)
    elif log_level == "debug":
        logger.setLevel(logging.DEBUG)

    logger.info(f"Loading {len(json_files)} JSON files into {database_filename}")
    click.echo(f"Loading {len(json_files)} JSON files into {database_filename}")

    files_successful, num_gab_rows = parse_and_load_to_sqlite(json_files, database_filename)

    click.echo(f"Successfully parsed {files_successful} JSON files, resulting in {num_gab_rows} gabs in database {database_filename}")


if __name__ == '__main__':
    tidy_data()
