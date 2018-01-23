from tests import fix_client, fix_suite, fix_report_downloader, fix_report, fix_report_definition  # import is used
import pytest


def test_init(fix_suite):
    from adobe_analytics.report_downloader import ReportDownloader

    ReportDownloader(fix_suite)


def test_to_report_from_report(fix_report_downloader, fix_report):
    assert fix_report == fix_report_downloader._to_report(fix_report)

# TODO: Create mock-requests for these tests, as they attempt to queue a report
# def test_to_report_from_report_def(fix_report_downloader, fix_report_definition):
#     from adobe_analytics.report_downloader import ReportDownloader
#
#     assert fix_report == fix_report_downloader._to_report(fix_report_definition)
#
#
# def test_to_report_from_report_dict(fix_report_downloader, fix_report_definition):
#     from adobe_analytics.report_downloader import ReportDownloader
#
#     dict_def = fix_report_definition.to_dict()
#     assert fix_report == fix_report_downloader._to_report(dict_def)


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
