from adobe_analytics import base_dir
import pytest
import requests_mock

test_dir = base_dir+"/tests"
mock_dir = test_dir+"/mock_objects"

test_suite_id = "omniture.api-gateway"


@pytest.fixture()
def fix_client():
    from adobe_analytics import Client

    with requests_mock.mock() as m:
        add_mock_requests_basic(mock_context=m)

        credentials_path = mock_dir+"/_login.json"
        client = Client.from_json(file_path=credentials_path)

        # results of the following method calls are cached
        # and used in further tests
        suite = client.suites()[test_suite_id]
        suite.metrics()
        suite.dimensions()
        suite.segments()
        return client


@pytest.fixture()
def fix_suite(fix_client):
    return fix_client.suites()[test_suite_id]


@pytest.fixture()
def fix_report_downloader(fix_suite):
    from adobe_analytics.report_downloader import ReportDownloader
    return ReportDownloader(fix_suite)


@pytest.fixture()
def fix_report_definition():
    from adobe_analytics.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        date_from="2017-01-01",
        date_to="2017-12-31"
    )
    return definition


def add_mock_requests_basic(mock_context):
    base_methods = [
        "Company.GetReportSuites",
        "Report.GetMetrics",
        "Report.GetElements",
        "Segments.Get"
    ]

    for method in base_methods:
        mock_response_file_name = method+".json"
        mock_response_path = mock_dir+"/"+mock_response_file_name
        with open(mock_response_path) as fh:
            response = fh.read()

            test_endpoint = 'https://api.omniture.com/admin/1.4/rest/?method='+method
            mock_context.post(test_endpoint, text=response)


def add_mock_request_queue(mock_context):
    mock_response_path = mock_dir+"/Report.Queue.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = 'https://api.omniture.com/admin/1.4/rest/?method=Report.Queue'
    mock_context.post(test_endpoint, text=response)


def add_mock_request_get_success(mock_context):
    mock_response_path = mock_dir+"/Report.Get.Ready.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = 'https://api.omniture.com/admin/1.4/rest/?method=Report.Get'
    mock_context.post(test_endpoint, text=response)


def add_mock_request_get_fail(mock_context):
    mock_response_path = mock_dir+"/Report.Get.NotReady.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = 'https://api.omniture.com/admin/1.4/rest/?method=Report.Get'
    mock_context.post(test_endpoint, text=response)


def add_mock_request_cancel_success(mock_context):
    test_endpoint = 'https://api.omniture.com/admin/1.4/rest/?method=Report.Cancel'
    mock_context.post(test_endpoint, text="true")
