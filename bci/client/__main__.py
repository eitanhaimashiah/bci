import click
import sys

from . import upload_sample
from ..utils.cli import main, log


@main.command('upload-sample')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--format', '-f')
@click.argument('path', type=click.Path())
def cli_upload_sample(host, port, format, path):
    upload_sample(host=host, port=port, format=format, path=path)


if __name__ == '__main__':
    try:
        main(prog_name='bci.client')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
