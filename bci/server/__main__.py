import click
import sys

from .server import run_server
from ..utils.cli import main, log
from ..publisher import Publisher


@main.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('url', required=False)
def cli_run_server(host, port, url):
    publisher = Publisher(url)

    def publish(message):
        # TODO Make sure the exchange and routing_key are correct
        publisher.publish(message,
                          exchange='snapshots',
                          routing_key='snapshot.data')

    run_server(host=host, port=port, publish=publish)


if __name__ == '__main__':
    try:
        main(prog_name='bci.server')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
