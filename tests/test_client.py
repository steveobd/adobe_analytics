#!/usr/bin/python
from tests import fix_client, test_suite_id  # import is used


def test_suites_is_dict(fix_client):
    assert isinstance(fix_client.suites, dict)


def test_suite_is_suite(fix_client):
    from adobe_analytics.suite import Suite

    fix_suite = fix_client.suites[test_suite_id]
    assert isinstance(fix_suite, Suite)


def test_request_without_auth(fix_client):
    import re

    pattern = r"https://api\d?.omniture.com/admin/1.4/rest/"
    response = fix_client.request(api="Company", method="GetEndpoint")
    assert re.match(pattern, response)
