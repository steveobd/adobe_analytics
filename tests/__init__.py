import pandas as pd
import pytest
import requests_mock

from adobe_analytics import base_dir

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
    from adobe_analytics.reports.report_downloader import ReportDownloader
    return ReportDownloader(fix_suite)


@pytest.fixture()
def fix_report_definition():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        date_from="2017-01-01",
        date_to="2017-12-31"
    )
    return definition


@pytest.fixture()
def fix_classification_uploader(fix_client):
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=["Key", "product_code"])

    uploader = ClassificationUploader(
        client=fix_client,
        suite_ids=["omniture.api-gateway"],
        variable_id="product",
        data=df,
        email="barack.obama@gmail.com",
        description="",
        check_suite_compatibility=True,
        export_results=False,
        overwrite_conflicts=True
    )
    return uploader


@pytest.fixture()
def fix_classification_job(fix_client):
    from adobe_analytics.classifications.classification_job import ClassificationJob

    job = ClassificationJob(
        client=fix_client,
        job_id=987
    )
    return job


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

            test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method="+method
            mock_context.post(test_endpoint, text=response)


def add_mock_request_queue(mock_context):
    mock_response_path = mock_dir+"/Report.Queue.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Report.Queue"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_get_success(mock_context):
    mock_response_path = mock_dir+"/Report.Get-2dim.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Report.Get"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_get_fail(mock_context):
    mock_response_path = mock_dir+"/Report.Get-not_ready.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Report.Get"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_cancel_success(mock_context):
    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Report.Cancel"
    mock_context.post(test_endpoint, text="true")


def add_mock_request_get_dwh_1page(mock_context):
    mock_response_path = mock_dir + "/Report.Get-warehouse_1page.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Report.Get"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_classification_create_import(mock_context):
    mock_response_path = mock_dir + "/Classifications.CreateImport.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Classifications.CreateImport"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_classification_add_data(mock_context):
    mock_response_path = mock_dir + "/Classifications.PopulateImport.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Classifications.PopulateImport"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_classification_commit_job(mock_context):
    mock_response_path = mock_dir + "/Classifications.CommitImport.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Classifications.CommitImport"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_classification_get_status_in_progress(mock_context):
    mock_response_path = mock_dir + "/Classifications.GetStatus-in_progress.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Classifications.GetStatus"
    mock_context.post(test_endpoint, text=response)


def add_mock_request_classification_get_status_done(mock_context):
    mock_response_path = mock_dir + "/Classifications.GetStatus-done.json"
    with open(mock_response_path) as fh:
        response = fh.read()

    test_endpoint = "https://api.omniture.com/admin/1.4/rest/?method=Classifications.GetStatus"
    mock_context.post(test_endpoint, text=response)
