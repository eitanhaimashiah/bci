import click
import sys

from . import Saver
from ..utils.cli import main, log
from ..publisher import Publisher


@main.command('save')
@click.option('--database', '-d')
@click.argument('topic')
@click.argument('path', type=click.Path())
def cli_save(database, topic, path):
    with open(path, 'r') as f:
        data = f.read()
    saver = Saver(database)
    saver.save(topic=topic, data=data)


@main.command('run-saver')
@click.argument('db_url', required=False)
@click.argument('mq_url', required=False)
def cli_run_saver(db_url, mq_url):
    saver = Saver(db_url)
    publisher = Publisher(mq_url, is_subscriber=True)

    def consume_callback(channel, method, properties, body):
        topic, _ = method.routing_key.split('.')
        saver.save(topic=topic, data=body)

    publisher.subscribe(exchange='results',
                        routing_key=f'*.result',
                        queue='saver',
                        callback=consume_callback)


if __name__ == '__main__':
    try:
        main(prog_name='bci.saver')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
