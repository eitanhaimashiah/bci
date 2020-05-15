import click
import sys

from .server import run_server
from ..utils.cli import main, log
# from ..publisher import find_publisher


@main.command('run-server')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('url', required=False)
def cli_run_server(host, port, url):
    # TODO Delete these two lines (just for debugging purposes)
    from bci.protocol.utils.display import display_snapshot
    run_server(host=host, port=port, publish=display_snapshot)

    # publisher = find_publisher(url)
    #
    # # TODO Recheck this code
    # publish = publisher(url,
    #                     pub_exchange='snapshots',
    #                     pub_routing_key='snapshot.data').publish
    # run_server(host, port, publish)


if __name__ == '__main__':
    try:
        main(prog_name='bci.server')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
