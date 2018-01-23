#!/usr/bin/python
from tests import fix_client  # import is used
from tests import test_suite_id, mock_dir


def test_fom_json():
    from adobe_analytics import Client

    json_path = mock_dir+"/login_dummy.json"
    client = Client.from_json(json_path)
    assert client.username == "my_username"
    assert client.password == "my_password"


def test_suites_is_dict(fix_client):
    assert isinstance(fix_client.suites(), dict)


def test_suite_is_suite(fix_client):
    from adobe_analytics.suite import Suite

    fix_suite = fix_client.suites[test_suite_id]
    assert isinstance(fix_suite, Suite)


def test_request_without_auth(fix_client):
    import re

    pattern = r"https://api\d?.omniture.com/admin/1.4/rest/"
    response = fix_client.request(api="Company", method="GetEndpoint")
    assert re.match(pattern, response)
