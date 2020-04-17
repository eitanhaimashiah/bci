import click
import sys

from . import read
from ..utils.cli import main, log


@main.command('read')
@click.option('--format', '-f')
@click.argument('path', type=click.Path())
def cli_read(format, path):
    log(read(format=format, path=path))


if __name__ == '__main__':
    try:
        main(prog_name='bci.reader')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
