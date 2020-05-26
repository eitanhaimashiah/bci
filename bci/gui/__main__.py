import click
import sys

from . import run_server
from ..utils.cli import main, log


@main.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--api-host', '-H')
@click.option('--api-port', '-P', type=int)
def cli_run_server(host, port, api_host, api_port):
    run_server(host=host,
               port=port,
               api_host=api_host,
               api_port=api_port)


if __name__ == '__main__':
    try:
        main(prog_name='bci.gui')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
