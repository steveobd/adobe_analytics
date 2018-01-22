from __future__ import absolute_import
from __future__ import print_function
import time
import functools

from adobe_analytics.report_downloader import ReportDownloader
from adobe_analytics.report_definition import ReportDefinition
from adobe_analytics.report import Report


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Suite(object):
    def __init__(self, name, suite_id, client):
        self.name = name
        self.id = suite_id
        self.client = client
        self.downloader = ReportDownloader(self)

    @classmethod
    def from_dict(cls, suite, client):
        return cls(name=suite['site_title'], suite_id=suite['rsid'], client=client)

    @functools.lru_cache(maxsize=None)
    def metrics(self):
        response = self.client.request(
            api='Report',
            method='GetMetrics',
            data={
                "reportSuiteID": self.id
            }
        )
        return self._response_to_dict(response)

    @functools.lru_cache(maxsize=None)
    def dimensions(self):
        response = self.client.request(
            api='Report',
            method='GetElements',
            data={
                "reportSuiteID": self.id
            }
        )
        return self._response_to_dict(response)

    @functools.lru_cache(maxsize=None)
    def segments(self):
        response = self.client.request(
            api='Segments',
            method='Get',
            data={
                "accessLevel": "shared"
            }
        )
        return self._response_to_dict(response)

    @staticmethod
    def _response_to_dict(data):
        return {item["id"]: item for item in data}

    def download_report(self, definition):
        report = self.download_report_async(definition)
        report.raw_data = self.downloader.check_until_ready(report)
        report.parse()
        return report

    def download_report_async(self, definition):
        report = Report.from_universal_definition_and_suite(definition, suite=self)
        report.id = self.downloader.queue(report)
        return report

    def __repr__(self):
        return "{name} ({id})".format(id=self.id, name=self.name)
