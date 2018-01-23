import requests_mock

from tests import fix_client, fix_suite, fix_report_definition, fix_report_downloader, fix_report  # import is used
from tests import add_mock_request_queue, add_mock_request_get_success


def test_response_to_dict():
    from adobe_analytics.suite import Suite
    response = [{
        "id": "pageviews",
        "name": "Page Views"
    }, {
        "id": "evar1",
        "name": "visit intend"
    }]
    result = Suite._response_to_dict(response)

    expected_result = {
        "pageviews": {
            "id": "pageviews",
            "name": "Page Views"
        },
        "evar1": {
            "id": "evar1",
            "name": "visit intend"
        }
    }
    assert result == expected_result


def test_metrics_is_dict(fix_suite):
    assert isinstance(fix_suite.metrics(), dict)


def test_elements_is_dict(fix_suite):
    assert isinstance(fix_suite.dimensions(), dict)


def test_segments_is_dict(fix_suite):
    assert isinstance(fix_suite.segments(), dict)


def test_download(fix_suite, fix_report):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)
        add_mock_request_get_success(mock_context)

        report = fix_suite.download(fix_report)
        assert report.dataframe is not None


def test_queue(fix_report_definition, fix_report_downloader):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report = fix_report_downloader.queue(fix_report_definition)
        assert report.id == 123