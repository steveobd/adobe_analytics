from tests import fix_client, test_suite_id  # import is used


def test_metrics_is_dict(fix_client):
    fix_suite = fix_client.suites[test_suite_id]
    assert isinstance(fix_suite.metrics(), dict)


def test_elements_is_dict(fix_client):
    fix_suite = fix_client.suites[test_suite_id]
    assert isinstance(fix_suite.dimensions(), dict)


def test_segments_is_dict(fix_client):
    fix_suite = fix_client.suites[test_suite_id]
    assert isinstance(fix_suite.segments(), dict)
