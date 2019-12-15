import os
import sys
import traceback
import click
from bci import run_server, upload_thought, run_webserver, Reader, version


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


def splitted(address):
    host, port = address.split(':')
    return host, int(port)


@click.group()
@click.version_option(version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('run_server')
@click.argument('address')
@click.argument('data_dir')
def cli_run_server(address, data_dir):
    log(run_server(splitted(address), data_dir))


@main.command('upload_thought')
@click.argument('address')
@click.argument('user', type=int)
@click.argument('thought')
def cli_upload_thought(address, user, thought):
    log(upload_thought(splitted(address), user, thought))


@main.command('run_webserver')
@click.argument('address')
@click.argument('data_dir')
def cli_run_webserver(address, data_dir):
    log(run_webserver(splitted(address), data_dir))


@main.command('read')
@click.argument('path')
def read(path):
    reader = Reader(path)
    print(reader.user_info())
    for snapshot in reader:
        print(snapshot)


if __name__ == '__main__':
    try:
        main(prog_name='bci', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
