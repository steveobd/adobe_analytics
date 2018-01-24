import requests_mock
import pytest

from tests import fix_client, fix_suite, fix_report_downloader, fix_report, fix_report_definition  # import is used
from tests import (add_mock_request_queue, add_mock_request_get_success,
                   add_mock_request_get_fail, add_mock_request_cancel_success)


def test_init(fix_suite):
    from adobe_analytics.report_downloader import ReportDownloader

    ReportDownloader(fix_suite)


def test_to_report_from_report(fix_report_downloader, fix_report):
    assert fix_report == fix_report_downloader._to_report(fix_report)


def test_to_report_from_report_def(fix_report_downloader, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report = fix_report_downloader._to_report(fix_report_definition)
        assert report.id == 123


def test_to_report_from_report_dict(fix_report_downloader, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report_definition = fix_report_definition.to_dict()
        report = fix_report_downloader._to_report(report_definition)
        assert report.id == 123


def test_to_report_from_int(fix_report_downloader):
    from adobe_analytics.report import Report

    result = fix_report_downloader._to_report(1489342)
    assert isinstance(result, Report)
    assert result.id == 1489342


def test_to_report_from_float(fix_report_downloader):
    from adobe_analytics.report import Report

    result = fix_report_downloader._to_report(1489342.0)
    assert isinstance(result, Report)
    assert result.id == 1489342


def test_build_request_data_definition(fix_report_definition):
    from adobe_analytics.report_downloader import ReportDownloader
    from adobe_analytics.report_definition import ReportDefinition

    filled_definition = ReportDefinition.inject_suite_id(fix_report_definition, "yooyoy")
    result = ReportDownloader._build_request_data_definition(filled_definition)
    assert result == {"reportDescription": filled_definition}


def test_build_request_data_definition_without_suite_id(fix_report_definition):
    from adobe_analytics.report_downloader import ReportDownloader

    with pytest.raises(AssertionError):
        ReportDownloader._build_request_data_definition(fix_report_definition)


def test_build_request_data_id(fix_report):
    from adobe_analytics.report_downloader import ReportDownloader

    result = ReportDownloader._build_request_data_id(fix_report)
    assert result == {"reportID": 123}


def test_queue(fix_report_downloader, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        dict_def = fix_report_definition.to_dict()
        report = fix_report_downloader.queue(dict_def)
        assert report.id == 123


def test_check_success(fix_report_downloader, fix_report):
    with requests_mock.mock() as mock_context:
        add_mock_request_get_success(mock_context)

        response = fix_report_downloader.check(fix_report)
        assert isinstance(response, dict)


def test_check_fail(fix_report_downloader, fix_report):
    with requests_mock.mock() as mock_context:
        add_mock_request_get_fail(mock_context)

        response = fix_report_downloader.check(fix_report)
        assert response is None


def test_download_with_report(fix_report_downloader, fix_report):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)
        add_mock_request_get_success(mock_context)

        report = fix_report_downloader.download(fix_report)
        assert report.dataframe is not None


def test_sleep_interval():
    from adobe_analytics.report_downloader import ReportDownloader

    assert ReportDownloader._sleep_interval(0) == 5
    assert ReportDownloader._sleep_interval(1) == 10
    assert ReportDownloader._sleep_interval(2) == 20


def test_check_until_ready(monkeypatch, fix_report_downloader, fix_report):
    import time
    monkeypatch.setattr(time, "sleep", lambda x: None)

    with requests_mock.mock() as mock_context:
        add_mock_request_get_fail(mock_context)

        response = fix_report_downloader.check_until_ready(fix_report, max_attempts=2)
        assert response is None


def test_cancel(fix_report_downloader, fix_report):
    with requests_mock.mock() as mock_context:
        add_mock_request_cancel_success(mock_context)

        response = fix_report_downloader.cancel(fix_report)
        assert isinstance(response, bool)
        assert response
