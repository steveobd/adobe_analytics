import pandas as pd
import numpy as np

import pytest
import requests_mock

from tests import fix_client, fix_classification_uploader, fix_classification_job
from tests import (add_mock_request_classification_create_import,
                   add_mock_request_classification_add_data,
                   add_mock_request_classification_commit_job,
                   add_mock_request_classification_get_status_done)


def test_validate_data_ok():
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=["Key", "product_code"])
    ClassificationUploader._validate_data(df)


def test_validate_data_no_df():
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = [
        [1, 2],
        [3, 4]
    ]
    with pytest.raises(AssertionError):
        ClassificationUploader._validate_data(df)


def test_validate_data_no_key():
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=["product", "product_code"])
    with pytest.raises(AssertionError):
        ClassificationUploader._validate_data(df)


def test_validate_data_has_nan():
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = pd.DataFrame([
        [1, 2],
        [3, np.nan]
    ], columns=["Key", "product_code"])
    with pytest.raises(AssertionError):
        ClassificationUploader._validate_data(df)


def test_header_and_values():
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    df = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=["Key", "product_code"])
    result_header, result_values = ClassificationUploader._header_and_values(df)
    assert result_header == ["Key", "product_code"]
    assert result_values == [[1, 2], [3, 4]]


def test_upload(fix_classification_uploader):
    with requests_mock.mock() as mock_context:
        add_mock_request_classification_create_import(mock_context)
        add_mock_request_classification_add_data(mock_context)
        add_mock_request_classification_commit_job(mock_context)
        add_mock_request_classification_get_status_done(mock_context)

        fix_classification_uploader.upload()


def test_create_import(fix_classification_uploader):
    from adobe_analytics.classifications.classification_job import ClassificationJob

    with requests_mock.mock() as mock_context:
        add_mock_request_classification_create_import(mock_context)
        result = fix_classification_uploader._create_import()

    assert isinstance(result, ClassificationJob)
    assert result.id == 987


def test_check_status_until_finished(fix_classification_job):
    from adobe_analytics.classifications.classification_uploader import ClassificationUploader

    with requests_mock.mock() as mock_context:
        add_mock_request_classification_get_status_done(mock_context)
        ClassificationUploader.check_status_until_finished(fix_classification_job)
