import os
import sys
import traceback
import click

from ..defaults import DEFAULT_QUIET, DEFAULT_TRACEBACK


class Log:
    """Warps commands' output to provide the functionality of the
    `quiet` and `traceback` flags.

    Attributes:
        quiet (bool): Flag indicating whether to quiet errors.
        traceback (bool): Flag indicating whether to print the
            traceback in case of an error.

    """

    def __init__(self):
        self.quiet = DEFAULT_QUIET
        self.traceback = DEFAULT_TRACEBACK

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(click.style(message, fg='red'))


log = Log()


@click.group()
@click.option('--quiet', '-q', is_flag=True, default=DEFAULT_QUIET)
@click.option('--traceback', '-t', is_flag=True, default=DEFAULT_TRACEBACK)
def main(quiet, traceback):
    log.quiet = quiet
    log.traceback = traceback
