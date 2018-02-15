import pandas as pd
import requests_mock

from tests import add_mock_request_queue, add_mock_request_get_success, add_mock_request_cancel_success
from tests import fix_client, fix_suite, fix_report_definition  # imports are used



def test_representation(fix_suite):
    assert fix_suite.__repr__() == "test_suite (omniture.api-gateway)"


def test_response_to_dict():
    from adobe_analytics.reports.suite import Suite
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


def test_download(fix_suite):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)
        add_mock_request_get_success(mock_context)

        df = fix_suite.download(123)
        assert isinstance(df, pd.DataFrame)


def test_queue(fix_suite, fix_report_definition):
    with requests_mock.mock() as mock_context:
        add_mock_request_queue(mock_context)

        report_id = fix_suite.queue(fix_report_definition)
        assert report_id == 123


def test_cancel(fix_suite):
    with requests_mock.mock() as mock_context:
        add_mock_request_cancel_success(mock_context)

        response = fix_suite.cancel(123)
        assert isinstance(response, bool)
        assert response
