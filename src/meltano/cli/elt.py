import os
import logging
import click
import datetime
from retrying import retry

from . import cli
from .add import add_plugin, add_transform
from .params import db_options, project
from meltano.core.config_service import ConfigService
from meltano.core.runner.singer import SingerRunner
from meltano.core.runner.dbt import DbtRunner
from meltano.core.project import Project, ProjectNotFound
from meltano.core.plugin import PluginType, ELTContext, infer_plugin_name
from meltano.core.plugin.error import PluginMissingError
from meltano.core.transform_add_service import TransformAddService
from meltano.core.tracking import GoogleAnalyticsTracker
from meltano.core.db import project_engine


@cli.command()
@click.argument("extractor")
@click.argument("loader")
@click.option("--dry", help="Do not actually run.", is_flag=True)
@click.option("--transform", type=click.Choice(["skip", "only", "run"]), default="skip")
@click.option(
    "--job_id", envvar="MELTANO_JOB_ID", help="A custom string to identify the job."
)
@db_options
@project
def elt(project, extractor, loader, dry, transform, job_id, engine_uri):
    """
    meltano elt EXTRACTOR_NAME LOADER_NAME

    extractor_name: Which extractor should be used in this extraction
    loader_name: Which loader should be used in this extraction
    """
    config_service = ConfigService(project)

    # register the project engine
    project_engine(project, engine_uri, default=True)
    install_missing_plugins(project, extractor, loader, transform)

    if job_id is None:
        # Autogenerate a job_id if it is not provided by the user
        job_id = f'job_{datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")}'

    singer_runner = SingerRunner(
        project,
        job_id=job_id,
        run_dir=os.getenv("SINGER_RUN_DIR", project.meltano_dir("run")),
        target_config_dir=project.meltano_dir(PluginType.LOADERS, loader),
        tap_config_dir=project.meltano_dir(PluginType.EXTRACTORS, extractor),
    )

    dbt_runner = DbtRunner(project)

    extractor_plugin = get_or_install_plugin(config_service, PluginType.EXTRACTORS, extractor)
    loader_plugin = get_or_install_plugin(config_service, PluginType.LOADERS, loader)
    transformer_plugin = get_or_install_plugin(config_service, PluginType.TRANSFORMERS, "dbt")

    elt_context = ELTContext.merge(extractor_plugin.elt_context,
                                    loader_plugin.elt_context,
                                    transformer_plugin.elt_context)

    try:
        if transform != "only":
            click.echo("Running extract & load...")
            singer_runner.run(extractor, loader, dry_run=dry)
            click.secho("Extract & load complete!", fg="green")
        else:
            click.secho("Extract & load skipped.", fg="yellow")

        if transform != "skip":
            click.echo("Running transformation...")
            dbt_runner.run(dry_run=dry, models=elt_context.source_name)
            click.secho("Transformation complete!", fg="green")
        else:
            click.secho("Transformation skipped.", fg="yellow")
    except Exception as err:
        raise click.ClickException(
            f"ELT could not complete, an error happened during the process: {err}."
        )

    tracker = GoogleAnalyticsTracker(project)
    tracker.track_meltano_elt(extractor=extractor, loader=loader, transform=transform)


def install_missing_plugins(
    project: Project, extractor: str, loader: str, transform: str
):
    config_service = ConfigService(project)

    extractor_plugin = get_or_install_plugin(config_service, PluginType.EXTRACTORS, extractor)
    loader_plugin = get_or_install_plugin(config_service, PluginType.LOADERS, loader)
    transformer_plugin = None

    if transform != "skip":
        transformer_plugin = get_or_install_plugin(config_service, PluginType.TRANSFORMERS, "dbt")

        elt_context = ELTContext.merge(extractor_plugin.elt_context,
                                       loader_plugin.elt_context,
                                       transformer_plugin.elt_context)

        transform_add_service = TransformAddService(project)
        transform_name = infer_plugin_name(PluginType.TRANSFORMS, elt_context)
        transform_plugin = get_or_install_plugin(config_service, PluginType.TRANSFORMS, transform_name)

        # Update dbt_project.yml in case the vars values have changed in meltano.yml
        transform_add_service.update_dbt_project(transform_plugin)


@retry(stop_max_attempt_number=2)
def get_or_install_plugin(config_service, plugin_type, plugin_name):
    try:
        return config_service.get_plugin(plugin_type, plugin_name)
    except PluginMissingError as e:
        click.secho(
            f"{plugin_type} {plugin_name} is missing. Trying to install it.", fg="green"
            )
        add_plugin(config_service.project, plugin_type, plugin_name)

        # triggers the retry
        raise e
