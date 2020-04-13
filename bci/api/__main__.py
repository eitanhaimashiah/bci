import click
from . import run_api_server
from ..defaults import DEFAULT_API_SERVER_IP, DEFAULT_API_SERVER_PORT, DEFAULT_DATABASE


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--database', '-d')
def cli_upload_sample(host, port, database):
    run_api_server(host=host, port=port, database_url=database)


if __name__ == '__main__':
    cli(prog_name='bci.api')
