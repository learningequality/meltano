import pytest
import os
from click.testing import CliRunner

from meltano.cli import cli
from meltano.core.project import Project, ProjectNotFound


def test_init(test_dir):
    runner = CliRunner()

    # there are no project actually
    with pytest.raises(ProjectNotFound):
        Project.find()

    # create one with the CLI
    runner.invoke(cli, ["init", "test_project"])
    os.chdir("test_project")

    project = Project.find()

    files = (
        project.root.joinpath(file).resolve()
        for file in (
            "meltano.yml",
            "README.md",
            ".gitignore",
            "transform/dbt_project.yml",
            "transform/profile/profiles.yml",
        )
    )

    dirs = (
        project.root.joinpath(dir)
        for dir in (
            "model",
            "extract",
            "load",
            "transform",
            "transform/profile",
            "analyze",
            "notebook",
            "orchestrate",
        )
    )

    for file in files:
        assert file.is_file()

    for dir in dirs:
        assert dir.is_dir()
