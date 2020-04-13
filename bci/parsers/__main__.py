import click
from . import run_parser


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('topic')
@click.argument('path', type=click.Path())
def cli_parse(topic, path):
    with open(path, 'rb') as f:
        data = f.read()
    run_parser(topic=topic, data=data)


@cli.command('run-parser')
@click.argument('topic')
@click.argument('mq')
def cli_run_parser(topic, mq):
    # TODO support running the parser as a service,
    #  which works with a message queue indefinitely
    pass


if __name__ == '__main__':
    cli(prog_name='bci.parsers')
