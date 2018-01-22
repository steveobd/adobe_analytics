from __future__ import absolute_import
from __future__ import print_function
import functools

from adobe_analytics.report_downloader import ReportDownloader
from adobe_analytics.report import Report


class Suite(object):
    def __init__(self, name, suite_id, client):
        self.name = name
        self.id = suite_id
        self.client = client
        self._downloader = ReportDownloader(self)

    def download_report(self, definition=None, report_id=None):
        assert definition or report_id
        assert not (definition and report_id)

        if definition:
            report = self.queue_report(definition)
        else:
            report = Report(report_id=report_id)
        print("ReportID:", report.id)

        report.raw_response = self._downloader.check_until_ready(report)
        report.parse()
        return report

    def queue_report(self, definition):
        report = Report.from_universal_definition_and_suite(definition, suite=self)
        report.id = self._downloader.queue(report)
        return report

    @classmethod
    def _from_dict(cls, suite, client):
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

    def __repr__(self):
        return "{name} ({id})".format(id=self.id, name=self.name)
