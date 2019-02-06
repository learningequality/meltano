from pyhocon import ConfigFactory
from pathlib import Path
from enum import Enum

import json


class M5oCollectionParserError(Exception):
    def __init__(self, message, file_name, *args):
        self.message = message
        self.file_name = file_name
        super(M5oCollectionParserError, self).__init__(
            self.message, self.file_name, *args
        )


class M5oCollectionParserTypes(Enum):
    Dashboard = 'dashboard'
    Report = 'report'


class M5oCollectionParser:
    def __init__(self, directory, file_type):
        self.directory = directory
        self.file_type = file_type.value
        self.pattern = f"*.{self.file_type}.m5o"
        self.files = []

    def contents(self):
        files = self.parse();
        self.compile(files);
        return self.files

    def compile(self, files):
        self.files = files
        compiled_file_name = f"{self.file_type}s.m5oc"
        compiled_file_path = Path(self.directory).joinpath(compiled_file_name)
        compiled_file = open(compiled_file_path, "w")
        compiled_file.write(json.dumps(self.files))
        compiled_file.close()

    def parse(self):
        files = []
        file_list = list(Path(self.directory).glob(self.pattern))
        for file in file_list:
            file_name = file.parts[-1]
            file_contents = self.get_file_contents(file)
            parsed_file = self.parse_file_contents(file_contents)
            files.append(parsed_file)

        return files

    def get_file_contents(self, file_path):
        try:
            return ConfigFactory.parse_string(open(file_path, "r").read())
        except Exception as e:
            raise M5oCollectionParserError(str(e), str(file_path.parts[-1]))

    def parse_file_contents(self, file_contents):
        parsed = {}
        for prop_name, prop_def in file_contents.items():
            parsed[prop_name] = prop_def
        return parsed
