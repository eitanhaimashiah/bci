import click
from .reader import read


@click.group()
def reader():
    pass


@reader.command('read')
@click.argument('path', type=click.Path())
@click.argument('format')
def cli_read(path, format):
    read(path, format)


if __name__ == '__main__':
    reader(prog_name='bci.reader')
