import click
import sys

from . import Saver
from ..utils.cli import main, log


@main.command('save')
@click.option('--database', '-d')
@click.argument('topic')
@click.argument('path', type=click.Path())
def cli_save(database, topic, path):
    with open(path, 'rb') as f:
        data = f.read()
    saver = Saver(database)
    saver.save(topic, data)


@main.command('run-saver')
@click.argument('db')
@click.argument('mq')
def cli_run_saver(db, mq):
    # TODO Support running the saver as a service, which works with
    #  a message queue indefinitely; it is then the saver's
    #  responsibility to subscribe to all the relevant topics it is
    #  capable of consuming and saving to the database
    pass


if __name__ == '__main__':
    try:
        main(prog_name='bci.saver')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
