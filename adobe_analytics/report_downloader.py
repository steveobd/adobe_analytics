import time

from adobe_analytics.report import Report
from adobe_analytics.report_definition import ReportDefinition


class ReportDownloader:
    def __init__(self, suite):
        self.suite = suite

    def download(self, report_definition=None, report_id=None):
        assert report_definition or report_id
        assert not (report_definition and report_id)

        report = self._create_report(report_definition, report_id)
        print("ReportID:", report.id)  # TODO: should be logging

        report.raw_response = self.check_until_ready(report)
        report.parse()
        return report

    def _create_report(self, report_definition, report_id):
        if report_definition:
            report_definition = ReportDefinition.assert_dict(report_definition)
            report_id = self.queue(report_definition)
        return Report(report_id=report_id)

    def queue(self, report_definition):
        client = self.suite.client

        report_definition = ReportDefinition.inject_suite_id(report_definition, self.suite.id)
        request_data = self._build_request_data_definition(report_definition)
        response = client.request(
            api="Report",
            method="Queue",
            data=request_data
        )
        return response["reportID"]

    def check_until_ready(self, report):
        response = self.check(report)
        while response is None:
            time.sleep(30)
            response = self.check(report)
        return response

    def check(self, report):
        client = self.suite.client

        request_data = self._build_request_data_id(report)
        response = client.request(
            api="Report",
            method="Get",
            data=request_data
        )
        is_ready = ("error" not in response) or (response["error"] != "report_not_ready")
        if is_ready:
            return response
        return None

    def cancel(self, report):
        client = self.suite.client

        request_data = self._build_request_data_id(report)
        response = client.request(
            api='Report',
            method='Cancel',
            data=request_data
        )
        return response

    @staticmethod
    def _build_request_data_definition(report_definition):
        assert report_definition["reportSuiteID"] is not None
        return {'reportDescription': report_definition}

    @staticmethod
    def _build_request_data_id(report):
        return {'reportID': report.id}
