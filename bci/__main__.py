import click

from . import version


@click.group()
@click.version_option(version)
def main():
    pass


if __name__ == '__main__':
    main(prog_name='bci')
