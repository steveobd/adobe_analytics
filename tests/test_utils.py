import requests_mock
import pytest
import json
import pandas as pd
import numpy as np

from tests import mock_dir
from tests import fix_client, fix_suite, fix_report_downloader, fix_report_definition  # import is used
from tests import (add_mock_request_queue, add_mock_request_get_success,
                   add_mock_request_get_fail, add_mock_request_cancel_success,
                   add_mock_request_get_dwh_1page)


def test_queue_reports(fix_client, fix_report_definition):
    from adobe_analytics.utils import _queue_reports

    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        suite_ids = ["omniture.api-gateway"]
        suites = fix_client.suites()
        res = _queue_reports(suite_ids=suite_ids, suites=suites, report_definition=fix_report_definition)
        assert res == {"omniture.api-gateway": 123}


def test_download_reports(fix_client):
    from adobe_analytics.utils import _download_reports

    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)

        suite_ids = ["omniture.api-gateway"]
        suites = fix_client.suites()
        report_ids = {"omniture.api-gateway": 123}
        res = _download_reports(suite_ids=suite_ids, suites=suites, report_ids=report_ids)

        expected_result = pd.DataFrame([
            [np.nan, np.nan, "209726", "0"],
            [np.nan, "page1", "2", "2"],
            [np.nan, "page2", "2", "2"],
            [np.nan, "page3", "4", "8"],
            ["11911", "page4", "1", "1"],
            ["11911", "page5", "4", "5"],
            ["12900", "page6", "1", "1"]
        ], columns=["Unit Name", "Page", "Visits", "Page Views"])
        assert isinstance(res, list)
        assert len(res) == 1
        assert res[0].equals(expected_result)


def test_download_in_multiple_suites(fix_client, fix_report_definition):
    from adobe_analytics.utils import download_async

    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)
        add_mock_request_queue(mock_context)

        res = download_async(fix_client, fix_report_definition, suite_ids=["omniture.api-gateway"])

        expected_result = pd.DataFrame([
            [np.nan, np.nan, "209726", "0"],
            [np.nan, "page1", "2", "2"],
            [np.nan, "page2", "2", "2"],
            [np.nan, "page3", "4", "8"],
            ["11911", "page4", "1", "1"],
            ["11911", "page5", "4", "5"],
            ["12900", "page6", "1", "1"]
        ], columns=["Unit Name", "Page", "Visits", "Page Views"])
        assert res.equals(expected_result)
