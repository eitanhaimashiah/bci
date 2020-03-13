import click
from .client import upload_sample


@click.group()
def client():
    pass


@client.command('upload-sample')
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8000)
@click.option('--fmt', '-f', default='protobuf')
@click.argument('path', type=click.Path())
def cli_upload_sample(host, port, path, fmt):
    upload_sample(host, port, path, fmt)


if __name__ == '__main__':
    client(prog_name='bci.client', obj={})
