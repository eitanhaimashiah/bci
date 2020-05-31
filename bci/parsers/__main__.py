import click
import sys

from . import parse
from ..utils.cli import main, log
from ..publisher import Publisher


@main.command('parse')
@click.argument('topic')
@click.argument('path', type=click.Path())
def cli_parse(topic, path):
    with open(path, 'r') as f:
        data = f.read()
    return parse(field=topic, data=data)


@main.command('run-parser')
@click.argument('topic')
@click.argument('mq_url', required=False)
def cli_run_parser(topic, mq_url):
    publisher = Publisher(mq_url, is_subscriber=True)

    def consume_callback(channel, method, properties, body):
        result = parse(field=topic, data=body)
        publisher.publish(result,
                          exchange='results',
                          routing_key=f'{topic}.result')

    publisher.subscribe(exchange='snapshots',
                        routing_key='snapshot.raw',
                        queue=topic,
                        callback=consume_callback)


if __name__ == '__main__':
    try:
        main(prog_name='bci.parsers')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
