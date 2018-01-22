import time


class ReportDownloader:
    def __init__(self, suite):
        self.suite = suite

    def validate(self, report):
        client = self.suite.client

        request_data = self._build_request_data_definition(report)
        response = client.request(
            api="Request",
            method="Validate",
            data=request_data
        )
        return "valid" in response

    def queue(self, report):
        client = self.suite.client

        request_data = self._build_request_data_definition(report)
        response = client.request(
            api="Request",
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
    def _build_request_data_definition(report):
        return {'reportDescription': report.definition}

    @staticmethod
    def _build_request_data_id(report):
        return {'reportID': report.id}
