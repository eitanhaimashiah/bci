import click
import sys

from . import parse
from ..utils.cli import main, log
from ..publisher import Publisher


@main.command('parse')
@click.argument('field')
@click.argument('path', type=click.Path())
def cli_parse(field, path):
    with open(path, 'r') as f:
        data = f.read()
    return parse(field=field, data=data)


@main.command('run-parser')
@click.argument('field')
@click.argument('mq_url', required=False)
def cli_run_parser(field, mq_url):
    publisher = Publisher(mq_url, is_subscriber=True)

    def consume_callback(channel, method, properties, body):
        result = parse(field=field, data=body)
        publisher.publish(result,
                          exchange=field,
                          routing_key=f'{field}.result')

    publisher.subscribe(exchange='snapshots',
                        routing_key='snapshot.raw',
                        queue=field,
                        callback=consume_callback)


if __name__ == '__main__':
    try:
        main(prog_name='bci.parsers')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
