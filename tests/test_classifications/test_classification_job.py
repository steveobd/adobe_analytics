import requests_mock

from tests import (add_mock_request_classification_add_data,
                   add_mock_request_classification_commit_job,
                   add_mock_request_classification_get_status_done)
from tests import fix_client, fix_classification_job  # import is used


def test_to_labeled_rows():
    from adobe_analytics.classifications.classification_job import ClassificationJob

    values = [
        [1, 2],
        [3, 4]
    ]
    expected_result = [
        {
            "row": [
                1, 2
            ]
        },
        {
            "row": [
                3, 4
            ]
        }
    ]

    result = ClassificationJob._to_labeled_rows(values)
    assert result == expected_result


def test_add_data(fix_classification_job):
    from adobe_analytics.classifications.classification_job import ClassificationJob
    values = [[i, i+1] for i in range(ClassificationJob.MAX_PAGE_SIZE + 2)]

    with requests_mock.mock() as mock_context:
        add_mock_request_classification_add_data(mock_context)
        fix_classification_job.add_data(values)


def test_commit(fix_classification_job):
    with requests_mock.mock() as mock_context:
        add_mock_request_classification_commit_job(mock_context)
        assert fix_classification_job.commit()


def test_check_status(fix_classification_job):
    with requests_mock.mock() as mock_context:
        add_mock_request_classification_get_status_done(mock_context)
        assert fix_classification_job.check_status()
