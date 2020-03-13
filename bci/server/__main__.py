import click
from .server import run_server

@click.group()
def server():
    pass


@server.command('run-server')
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8000)
def cli_run_server(host, port):
    run_server(host, port)


if __name__ == '__main__':
    server(prog_name='bci.server', obj={})
