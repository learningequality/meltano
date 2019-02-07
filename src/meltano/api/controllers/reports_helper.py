import os
import json
from os.path import join
from pathlib import Path
from meltano.core.utils import slugify
from .m5o_collection_parser import M5oCollectionParser, M5oCollectionParserTypes
from .m5o_file_parser import MeltanoAnalysisFileParser


class ReportsHelper:
    def __init__(self):
        self.meltano_model_path = join(os.getcwd(), "model")
        self.report_version = "1.0.0"

    def get_reports(self):
        path = Path(self.meltano_model_path)
        reportsParser = M5oCollectionParser(path, M5oCollectionParserTypes.Report)
        return reportsParser.contents()

    def load_report(self, report_name):
        reports = self.get_reports()
        target_report = [report for report in reports if report["name"] == report_name]
        return target_report[0]

    def save_report(self, data):
        slug = slugify(data["name"])
        file_name = f"{slug}.report.m5o"
        file_path = Path(self.meltano_model_path).joinpath(file_name)
        data = MeltanoAnalysisFileParser.fill_base_m5o_dict(file_path, slug, data)
        data["version"] = self.report_version
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data

    def update_report(self, data):
        file_name = data["slug"] + ".report.m5o"
        file_path = Path(self.meltano_model_path).joinpath(file_name)
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data
