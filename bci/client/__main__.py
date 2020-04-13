import click
from . import upload_sample


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('--host', '-h')
@click.option('--port', '-p', type=int)
@click.option('--format', '-f')
@click.argument('path', type=click.Path())
def cli_upload_sample(host, port, format, path):
    upload_sample(host=host, port=port, format=format, path=path)


if __name__ == '__main__':
    cli(prog_name='bci.client')
