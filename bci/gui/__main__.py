import click
from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--api-host', '-H')
@click.option('--api-port', '-P', type=int)
def cli_run_server(host, port, api_host, api_port):
    run_server(host=host,
               port=port,
               api_host=api_host,
               api_port=api_port)


def print_message(message):
    print(message)


if __name__ == '__main__':
    cli(prog_name='bci.gui')
