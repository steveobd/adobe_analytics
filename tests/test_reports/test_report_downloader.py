import requests_mock
import pytest
import json
import pandas as pd
import numpy as np

from tests import mock_dir
from tests import fix_client, fix_suite, fix_report_downloader, fix_report_definition  # imports are used
from tests import (add_mock_request_queue, add_mock_request_get_success,
                   add_mock_request_cancel_success, add_mock_request_get_dwh_1page)


def test_init(fix_suite):
    from adobe_analytics.reports.report_downloader import ReportDownloader

    ReportDownloader(fix_suite)


def test_to_report_id_from_report_def(fix_report_downloader, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report_id = fix_report_downloader._to_report_id(fix_report_definition)
        assert report_id == 123


def test_to_report_id_from_int(fix_report_downloader):
    report_id = fix_report_downloader._to_report_id(1489342)
    assert report_id == 1489342


def test_to_report_id_from_float(fix_report_downloader):
    report_id = fix_report_downloader._to_report_id(1489342.0)
    assert report_id == 1489342


def test_build_request_data_definition(fix_report_definition):
    from adobe_analytics.reports.report_downloader import ReportDownloader
    from adobe_analytics.reports.report_definition import ReportDefinition

    filled_definition = ReportDefinition.inject_suite_id(fix_report_definition, "yooyoy")
    result = ReportDownloader._build_request_data_definition(filled_definition)
    assert result == {"reportDescription": filled_definition}


def test_build_request_data_definition_without_suite_id(fix_report_definition):
    from adobe_analytics.reports.report_downloader import ReportDownloader

    with pytest.raises(AssertionError):
        json_def = fix_report_definition.raw
        ReportDownloader._build_request_data_definition(json_def)


def test_queue(fix_report_downloader, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report_id = fix_report_downloader.queue(fix_report_definition)
        assert report_id == 123


def test_check_success(fix_report_downloader):
    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)

        response = fix_report_downloader.get_report(123)
        assert isinstance(response, dict)


def test_download_with_report_id(fix_report_downloader):
    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)

        df = fix_report_downloader.download(123)
        assert isinstance(df, pd.DataFrame)


def test_cancel(fix_report_downloader):
    with requests_mock.mock() as mock_context:
        add_mock_request_cancel_success(mock_context)

        response = fix_report_downloader.cancel(123)
        assert isinstance(response, bool)
        assert response


def test_to_stacked_dataframe():
    from adobe_analytics.reports.report_downloader import ReportDownloader

    file_path = mock_dir + "/Report.Get-2dim_and_granularity_missing_values.json"
    with open(file_path, mode="r") as json_file:
        raw_response = json.load(json_file)
    result = ReportDownloader._to_stacked_dataframe([raw_response, raw_response])

    expected_data = [
        ["2018-01-01 04:00:00", np.nan, "mkt1", "31"],
        ["2018-01-01 04:00:00", np.nan, "mkt2", "30"],
        ["2018-01-01 04:00:00", "product1", "mkt1", "28"],
        ["2018-01-01 04:00:00", "product1", "mkt2", "18"],
        ["2018-01-01 04:00:00", "product2", "mkt2", "11"]
    ]
    expected_result = pd.DataFrame(
        data=expected_data * 2,
        columns=["Datetime", "Product Name", "Last Touch Marketing Channel", "Visits"]
    )

    assert expected_result.equals(result)


def test_download_dwh_1page(fix_report_downloader):
    with requests_mock.mock() as mock_context:
        add_mock_request_get_dwh_1page(mock_context)

        df = fix_report_downloader.download(123)

    expected_result = pd.DataFrame([
        [np.nan, "383420"],
        ["11911", "4"]
    ], columns=["Page", "Page Views"])
    assert df.equals(expected_result)
