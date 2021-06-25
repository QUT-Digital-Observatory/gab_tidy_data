import click


@click.command()
@click.argument('json_files', type=click.File('r'), nargs=-1)
@click.argument('database_filename', type=click.Path(dir_okay=False, writable=True), required=True)
def tidy_data(json_files, database_filename):
    pass


if __name__ == '__main__':
    tidy_data()
