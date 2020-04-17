import click
import sys

from . import run_api_server
from ..utils.cli import main, log


@main.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--database', '-d')
def cli_upload_sample(host, port, database):
    run_api_server(host=host, port=port, database_url=database)


if __name__ == '__main__':
    try:
        main(prog_name='bci.api')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
