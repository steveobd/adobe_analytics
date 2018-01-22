import pandas as pd
import numpy as np

from adobe_analytics.report_definition import ReportDefinition


class Report:
    def __init__(self, definition=None, report_id=None):
        assert definition or report_id, "Provide either report_definition or report_id."
        if definition is not None:
            assert "reportSuiteID" in definition, "Must provide report suite id."

        self.definition = definition  # used by ReportDownloader. Q: Really necessary here?
        self.id = report_id
        self.raw_response = None

        self.dataframe = None

    @classmethod
    def from_universal_definition_and_suite(cls, definition, suite):
        report_definition = ReportDefinition.assert_dict(definition)
        report_definition["reportSuiteID"] = suite.id
        return Report(definition=report_definition)

    def parse(self):
        assert self.raw_response is not None, "Download report data first."
        raw_data = self.raw_response['report']["data"]

        dimensions, metrics = self._parse_header()
        data = self._parse_data(raw_data, metric_count=len(metrics))
        header = self._fix_header(dimensions, metrics, data)

        self.dataframe = pd.DataFrame(data, columns=header)

    @staticmethod
    def _fix_header(dimensions, metrics, data):
        header = dimensions + metrics
        if len(header) != len(data[0]):  # can only be when granularity breakdown is used
            return ["Granularity"] + header
        return header

    def _parse_header(self):
        report = self.raw_response['report']

        dimensions = [(e["classification"] if "classification" in e else e["name"]) for e in report["elements"]]
        metrics = [m["name"] for m in report["metrics"]]
        return dimensions, metrics

    def _parse_data(self, data, metric_count):
        """
        Recursive parsing of the "data" part of the Adobe response.
        :param data: list of dicts and lists. quite a complicated structure
        :param metric_count: int, number of metrics in report
        :return: list of lists
        """
        if "breakdown" in data[0]:
            rows = list()
            for chunk in data:
                dim_is_none = "name" not in chunk or chunk["name"] == ""
                dim_value = np.nan if dim_is_none else chunk["name"]
                rows += [[dim_value] + row
                         for row in self._parse_data(chunk["breakdown"], metric_count)]
            return rows
        else:
            return self._parse_most_granular(data, metric_count)

    def _parse_most_granular(self, data, metric_count):
        """
        Parsing of the most granular part of the response.
        It is different depending on if there's a granularity breakdown or not
        :param data: dict
        :param metric_count: int, number of metrics in report
        :return: list of lists
        """
        rows = list()
        for chunk in data:
            dim_name = chunk["name"] if chunk["name"] != "" else np.nan
            # data alignment is a bit different if adding granularity breakdowns
            part_rows = [(val if val != "" else np.nan) for val in chunk["counts"]]
            if len(chunk["counts"]) > metric_count:
                part_rows = self.chunks(part_rows, step_size=metric_count+1)
            else:
                part_rows = [part_rows]
            rows += [[dim_name]+part_row for part_row in part_rows]
        return rows

    @staticmethod
    def chunks(data, step_size):
        """Yield successive n-sized chunks from l."""
        return [data[i:i + step_size] for i in range(0, len(data), step_size)]
