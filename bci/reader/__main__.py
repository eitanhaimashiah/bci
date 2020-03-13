import click
from .reader import read


@click.group()
def reader():
    pass


@reader.command('read')
@click.argument('path', type=click.Path())
@click.argument('fmt')
def cli_read(path, fmt):
    read(path, fmt)


if __name__ == '__main__':
    reader(prog_name='bci.reader', obj={})
