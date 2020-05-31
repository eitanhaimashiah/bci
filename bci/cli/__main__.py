import click
import requests
import sys

from ..defaults import DEFAULT_API_SERVER_HOST, DEFAULT_API_SERVER_PORT
from ..utils.cli import main, log


@main.command('get-users')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
def cli_get_users(host, port):
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    url = f'http://{host}:{port}/users'
    click.echo(requests.get(url).text)


@main.command('get-user')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
def cli_get_user(host, port, user_id):
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    url = f'http://{host}:{port}/users/{user_id}'
    click.echo(requests.get(url).text)


@main.command('get-snapshots')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
def cli_get_snapshots(host, port, user_id):
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    url = f'http://{host}:{port}/users/{user_id}/snapshots'
    click.echo(requests.get(url).text)


@main.command('get-snapshot')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def cli_get_snapshot(host, port, user_id, snapshot_id):
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    click.echo(requests.get(url).text)


@main.command('get-result')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--save', '-s', type=click.Path(), default=None)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('topic')
def cli_get_result(host, port, save, user_id, snapshot_id, topic):
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{topic}'
    result = requests.get(url)
    if save:
        with open(save, 'wb') as f:
            f.write(result.content)
    else:
        click.echo(result.text)


if __name__ == '__main__':
    try:
        main(prog_name='bci.cli')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
