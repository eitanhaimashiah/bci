import click
from ..defaults import DEFAULT_API_SERVER_IP, DEFAULT_API_SERVER_PORT


@click.group()
def cli():
    pass


@cli.command('get-users')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
def cli_get_users(host, port):
    host = host or DEFAULT_API_SERVER_IP
    port = port or DEFAULT_API_SERVER_PORT
    # TODO Complete
    pass


@cli.command('get-user')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
def cli_get_user(host, port, user_id):
    host = host or DEFAULT_API_SERVER_IP
    port = port or DEFAULT_API_SERVER_PORT
    # TODO Complete
    pass


@cli.command('get-snapshots')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
def cli_get_snapshots(host, port, user_id):
    host = host or DEFAULT_API_SERVER_IP
    port = port or DEFAULT_API_SERVER_PORT
    # TODO Complete
    pass


@cli.command('get-snapshot')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def cli_get_snapshot(host, port, user_id, snapshot_id):
    host = host or DEFAULT_API_SERVER_IP
    port = port or DEFAULT_API_SERVER_PORT
    # TODO Complete
    pass


# TODO Accept the `-s/--save` flag properly
@cli.command('get-result')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('topic')
# @click.option('--save', '-s', type=bool)
# @click.argument('path')
def cli_get_result(host, port, user_id, snapshot_id, topic):
    host = host or DEFAULT_API_SERVER_IP
    port = port or DEFAULT_API_SERVER_PORT
    # TODO Complete
    pass


if __name__ == '__main__':
    cli(prog_name='bci.cli')
