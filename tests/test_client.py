#!/usr/bin/python
import pytest
import collections

from tests import mock_dir
from tests import fix_client, fix_suite  # imports are used


def test_fom_json():
    from adobe_analytics import Client

    json_path = mock_dir+"/_login.json"
    client = Client.from_json(json_path)
    assert client.username == "my_username"
    assert client.password == "my_password"


def test_suites_is_dict(fix_client):
    assert isinstance(fix_client.suites(), dict)


def test_suite_is_suite(fix_suite):
    from adobe_analytics.reports.suite import Suite

    assert isinstance(fix_suite, Suite)


def test_request_without_auth(fix_client):
    import re

    pattern = r"https://api\d?.omniture.com/admin/1.4/rest/"
    response = fix_client.request(api="Company", method="GetEndpoint", data={"company": "clearly"})
    assert re.match(pattern, response)


def test_serialize_header(fix_client):
    properties = collections.OrderedDict([("a", "yo1"), ("b", "yo2")])
    result = fix_client._serialize_header(properties)
    assert result == 'a="yo1", b="yo2"'


def test_client_representation(fix_client):
    result = fix_client.__repr__()
    assert result == "User: my_username | Endpoint: https://api.omniture.com/admin/1.4/rest/"


def test_raise_error_report_not_ready():
    from adobe_analytics.client import Client

    response = {
        "error": "report_not_ready",
        "error_description": "Report not ready",
        "error_uri": None
    }
    with pytest.raises(FileNotFoundError):
        Client.raise_error(response)


def test_raise_error_other_error():
    from adobe_analytics.client import Client

    response = {
        "error": "Bad Request",
        "error_description": "Authentication key not found",
        "error_uri": None
    }
    with pytest.raises(Exception):
        Client.raise_error(response)
