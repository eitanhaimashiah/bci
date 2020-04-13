import click
from . import Saver


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('--database', '-d')
@click.argument('topic')
@click.argument('path', type=click.Path())
def cli_save(database, topic, path):
    with open(path, 'rb') as f:
        data = f.read()
    saver = Saver(database)
    saver.save(topic, data)


@cli.command('run-saver')
@click.argument('db')
@click.argument('mq')
def cli_run_saver(db, mq):
    # TODO Support running the saver as a service, which works with
    #  a message queue indefinitely; it is then the saver's
    #  responsibility to subscribe to all the relevant topics it is
    #  capable of consuming and saving to the database
    pass


if __name__ == '__main__':
    cli(prog_name='bci.saver')
