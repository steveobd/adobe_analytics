from adobe_analytics import base_dir
import pytest
import requests_mock

test_dir = base_dir+"/tests"
mock_dir = test_dir+"/mock_objects"

test_suite_id = "omniture.api-gateway"


@pytest.fixture(scope="module")
def fix_client():
    from adobe_analytics import Client

    with requests_mock.mock() as m:
        initiate_base_mock_responses(mock_context=m)

        credentials_path = mock_dir+"/login.json"
        client = Client.from_json(file_path=credentials_path)

        # results of the following method calls are cached
        # and used in further tests
        suite = client.suites()[test_suite_id]
        suite.metrics()
        suite.dimensions()
        suite.segments()
        return client


def initiate_base_mock_responses(mock_context):
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