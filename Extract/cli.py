import click
from Extract.fastly.extractor import FastlyExtractor


@click.group()
def cli():
    click.echo("cli group")
    pass


@click.command()
def extract():
    click.echo('Extracting ...')
    fastly = FastlyExtractor()
    res = fastly.extract()
    print(res)


cli.add_command(extract)

if __name__ == '__main__':
    cli()
