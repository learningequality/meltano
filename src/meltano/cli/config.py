import click
import json

from . import cli
from .params import project

from meltano.core.db import project_engine
from meltano.core.project import Project
from meltano.core.project_settings_service import ProjectSettingsService
from meltano.core.plugin import PluginType
from meltano.core.plugin.error import PluginMissingError
from meltano.core.config_service import ConfigService
from meltano.core.plugin.settings_service import (
    PluginSettingsService,
    SpecificPluginSettingsService,
    SettingValueStore,
)


@cli.group(invoke_without_command=True)
@click.option(
    "--plugin-type", type=click.Choice(PluginType.cli_arguments()), default=None
)
@click.argument("plugin_name")
@click.option("--format", type=click.Choice(["json", "env"]), default="json")
@project(migrate=True)
@click.pass_context
def config(ctx, project, plugin_type, plugin_name, format):
    try:
        plugin_type = PluginType.from_cli_argument(plugin_type) if plugin_type else None

        config = ConfigService(project)
        plugin = config.find_plugin(
            plugin_name, plugin_type=plugin_type, configurable=True
        )
    except PluginMissingError:
        plugin = None
        if plugin_name == "meltano":
            path_prefix = []
        else:
            path_prefix = [plugin_name]

    _, Session = project_engine(project)
    session = Session()
    try:
        if plugin:
            settings = PluginSettingsService(project).build(session, plugin)
        else:
            settings = ProjectSettingsService(
                project, session=session, path_prefix=path_prefix
            )

        ctx.obj["settings"] = settings

        if ctx.invoked_subcommand is None:
            if format == "json":
                config = settings.as_config()
                print(json.dumps(config))
            elif format == "env":
                for env, value in settings.as_env().items():
                    print(f"{env}={value}")
    finally:
        session.close()


@config.command()
@click.argument("setting_name", nargs=-1, required=True)
@click.argument("value")
@click.option(
    "--store",
    type=click.Choice(list(SettingValueStore)),
    default=SettingValueStore.MELTANO_YML,
)
@click.pass_context
def set(ctx, setting_name, value, store):
    path = list(setting_name)
    ctx.obj["settings"].set(path, value, store=store)


@config.command()
@click.argument("setting_name", nargs=-1, required=True)
@click.option(
    "--store",
    type=click.Choice(list(SettingValueStore)),
    default=SettingValueStore.MELTANO_YML,
)
@click.pass_context
def unset(ctx, setting_name, store):
    path = list(setting_name)
    ctx.obj["settings"].unset(path, store=store)


@config.command()
@click.option(
    "--store",
    type=click.Choice(list(SettingValueStore)),
    default=SettingValueStore.MELTANO_YML,
)
@click.pass_context
def reset(ctx, store):
    ctx.obj["settings"].reset(store=store)


@config.command("list")
@click.pass_context
def list_settings(ctx):
    settings = ctx.obj["settings"]
    for setting_def in settings.definitions():
        click.secho(setting_def.name, fg="blue", nl=False)

        env_key = settings.setting_env(setting_def)
        click.echo(f" [{env_key}]", nl=False)

        if setting_def.value is not None:
            click.echo(" (default: %r)" % setting_def.value, nl=False)

        if setting_def.description:
            click.echo(f": {setting_def.description}", nl=False)

        click.echo()
