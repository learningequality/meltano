import click

from Extract.fastly.extractor import FastlyExtractor
from Load.postgres import PostgresLoader

loaders_registry = {
    'postgres': PostgresLoader,
}
extractors_registry = {
    'fastly': FastlyExtractor,
}


@click.group()
def cli():
    click.echo("cli group")
    pass


@click.command()
@click.argument('extractor')
@click.option('--loader', default='postgres',
              help="Which loader should be used in this extraction")
def extract(extractor, loader):
    """
    Extractor expects name of the extractor as a first argument
    """
    click.echo("Starting extraction ...")
    extractor_class = extractors_registry.get(extractor)
    if not extractor_class:
        raise Exception(
            f'Extractor {extractor} not found please specify one of the following: {extractors_registry.keys()}')
    loader_class = loaders_registry.get(loader, None)
    if not loader_class:
        raise Exception(f'Loader {loader} not found please specify one of the following: {loaders_registry.keys()}')
    extractor = extractor_class()
    extracted_dfs = extractor.extract()
    click.echo("Got extractor results, loading them into the loader")

    loader = loader_class()
    loader.load(schema_name=extractor.name, dataframes=extracted_dfs)
    click.echo("Load done! Exiting")


cli.add_command(extract)

if __name__ == '__main__':
    cli()
