import requests_mock
import pandas as pd
import numpy as np

from tests import add_mock_request_queue, add_mock_request_get_success
from tests import fix_client, fix_report_definition  # imports are used



def test_queue_reports(fix_client, fix_report_definition):
    from adobe_analytics.reports.utils import _queue_reports

    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        suite_ids = ["omniture.api-gateway"]
        suites = fix_client.suites()
        res = _queue_reports(suite_ids=suite_ids, suites=suites, report_definition=fix_report_definition)
        assert res == {"omniture.api-gateway": 123}


def test_download_reports(fix_client):
    from adobe_analytics.reports.utils import _download_reports

    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)

        suite_ids = ["omniture.api-gateway"]
        suites = fix_client.suites()
        report_ids = {"omniture.api-gateway": 123}
        res = _download_reports(suite_ids=suite_ids, suites=suites, report_ids=report_ids)

        expected_result = pd.DataFrame([
            ["omniture.api-gateway", np.nan, np.nan, "209726", "0"],
            ["omniture.api-gateway", np.nan, "page1", "2", "2"],
            ["omniture.api-gateway", np.nan, "page2", "2", "2"],
            ["omniture.api-gateway", np.nan, "page3", "4", "8"],
            ["omniture.api-gateway", "11911", "page4", "1", "1"],
            ["omniture.api-gateway", "11911", "page5", "4", "5"],
            ["omniture.api-gateway", "12900", "page6", "1", "1"]
        ], columns=["Suite ID", "Unit Name", "Page", "Visits", "Page Views"])
        assert isinstance(res, list)
        assert len(res) == 1
        assert res[0].equals(expected_result)


def test_download_async(fix_client, fix_report_definition):
    from adobe_analytics.reports.utils import download_async

    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)
        add_mock_request_queue(mock_context)

        res = download_async(fix_client, fix_report_definition, suite_ids=["omniture.api-gateway"])

        expected_result = pd.DataFrame([
            ["omniture.api-gateway", np.nan, np.nan, "209726", "0"],
            ["omniture.api-gateway", np.nan, "page1", "2", "2"],
            ["omniture.api-gateway", np.nan, "page2", "2", "2"],
            ["omniture.api-gateway", np.nan, "page3", "4", "8"],
            ["omniture.api-gateway", "11911", "page4", "1", "1"],
            ["omniture.api-gateway", "11911", "page5", "4", "5"],
            ["omniture.api-gateway", "12900", "page6", "1", "1"]
        ], columns=["Suite ID", "Unit Name", "Page", "Visits", "Page Views"])
        assert res.equals(expected_result)
