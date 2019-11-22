import datetime
import glob
import logging
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Union, Optional

from meltano.core.project import Project
from meltano.core.utils import slugify, makedirs


class MissingLogException(Exception):
    """Occurs when MeltanoUILoggingService can not find a requested log."""

    pass


class MeltanoUILoggingService:
    def __init__(self, project: Project):
        self.project = project

    @makedirs
    def meltano_ui_dir(self, *joinpaths):
        return self.project.run_dir("meltano_ui", *joinpaths)

    @contextmanager
    def create_log(self):
        """
        Open a new log file for logging and yield it.

        Log will be created inside the meltano_ui_dir: .meltano/run/meltano_ui/
        """
        file_name = f'{datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")}.log'
        log_file_name = self.meltano_ui_dir(file_name)

        try:
            log_file = open(log_file_name, "w")
        except (OSError, IOError) as err:
            # Don't stop the command running if you can not open the log file
            # for writting: just return /dev/null
            logging.error(
                f"Could open log file {log_file_name} for writting. Using /dev/null"
            )
            log_file = open(os.devnull, "w")

        try:
            yield log_file
        finally:
            log_file.close()

    def get_latest_log(self):
        """
        Get the contents of the most recent log for Meltano UI
        """
        try:
            latest_log = next(iter(self.get_all_logs()))
            with latest_log.open() as f:
                return f.read()
        except StopIteration:
            raise MissingLogException(f"Could not find any log for Meltano UI")
        except FileNotFoundError:
            raise MissingLogException(
                f"Cannot open Meltano UI log: '{latest_log}' is missing."
            )

    def get_all_logs(self):
        """
        Get all the log files for Meltano UI

        The result is ordered so that the most recent is first on the list
        """
        log_files = list(self.project.run_dir("meltano_ui").glob("**/*.log"))
        log_files.sort(key=lambda path: os.stat(path).st_ctime_ns, reverse=True)

        return log_files
