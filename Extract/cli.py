import click


@click.group()
def cli():
    click.echo("cli group")
    pass


@click.command()
def extract():
    click.echo('Extracting..')



cli.add_command(extract)

if __name__ == '__main__':
    cli()
