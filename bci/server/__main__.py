import click
from .server import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('mq')
def cli_run_server(host, port, mq):
    # TODO Run a message queue, and then pass the approripate publishing function
    run_server(host=host, port=port, publish=print_message)


def print_message(message):
    print(message)


if __name__ == '__main__':
    cli(prog_name='bci.server')
