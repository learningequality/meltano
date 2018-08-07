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
    :param extractor: name of the extractor
    :param loader: name of the loader
    :return:
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
    extracted_entities = extractor.extract()
    click.echo("Got extractor results, loading them into the loader")

    loader = loader_class()
    loader.load(extracted_entities)
    click.echo("Load done! Exiting")


cli.add_command(extract)

if __name__ == '__main__':
    cli()
