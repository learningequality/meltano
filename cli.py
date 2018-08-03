import os

import click

from fastly.extractor import FastlyExtractor


@click.group()
def cli():

    click.echo("cli group")
    print(os.environ.get('PYTHONPATH'))
    pass


@click.command()
def extract():

    click.echo("Extracting ...")
    fastly = FastlyExtractor()
    res = fastly.extract()
    click.echo("Got results, printing")
    print(res)


cli.add_command(extract)

if __name__ == '__main__':

    cli()
