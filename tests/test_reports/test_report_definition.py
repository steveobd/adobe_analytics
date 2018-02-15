import pytest

from tests import fix_report_definition  # imports are used


def test_init_dimensions_as_list():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions=["page", "product"],
        date_from="2017-01-01",
        date_to="2017-12-31"
    )
    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "page"
        }, {
            "id": "product"
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31"
    }
    assert definition.raw == expected_result


def test_init_dimensions_as_str():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="product",
        date_from="2017-01-01",
        date_to="2017-12-31"
    )
    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "product"
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31"
    }
    assert definition.raw == expected_result


def test_init_dimensions_as_list_of_dict():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions=[{
            "id": "product",
            "classification": "Product Name"
        }],
        date_from="2017-01-01",
        date_to="2017-12-31"
    )
    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "product",
            "classification": "Product Name"
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31"
    }
    assert definition.raw == expected_result


def test_init_no_metrics():
    from adobe_analytics.reports.report_definition import ReportDefinition

    with pytest.raises(TypeError):
        ReportDefinition(
            dimensions="product",
            last_days=7
        )


def test_init_no_dimensions():
    from adobe_analytics.reports.report_definition import ReportDefinition

    with pytest.raises(TypeError):
        ReportDefinition(
            metrics="pageviews",
            last_days=7
        )


def test_no_dates():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page"
    )

    with pytest.raises(AssertionError):
        _ = definition.raw


def test_abs_and_relative_dates():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        last_days=7,
        date_from="2017-01-01",
        date_to="2017-12-31"
    )

    with pytest.raises(AssertionError):
        _ = definition.raw


def test_dates_from_relative():
    from adobe_analytics.reports.report_definition import ReportDefinition
    import datetime

    today = datetime.date.today()
    yesterday = (today - datetime.timedelta(1)).isoformat()
    seven_days_ago = (today - datetime.timedelta(7)).isoformat()

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        last_days=7
    )
    definition._determine_dates()
    assert definition.date_from == seven_days_ago
    assert definition.date_to == yesterday


def test_with_segments():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        date_from="2017-01-01",
        date_to="2017-12-31",
        segments="2758295982395"
    )

    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "page",
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "segments": [{
           "id": "2758295982395"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31"
    }
    assert definition.raw == expected_result


def test_with_granularity():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        date_from="2017-01-01",
        date_to="2017-12-31",
        granularity="day"
    )

    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "page",
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31",
        "dateGranularity": "day"
    }
    assert definition.raw == expected_result


def test_with_sort_by():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        date_from="2017-01-01",
        date_to="2017-12-31",
        sortBy="pageviews"
    )

    expected_result = {
        "reportSuiteID": None,
        "elements": [{
            "id": "page",
        }],
        "metrics": [{
            "id": "pageviews"
        }],
        "dateFrom": "2017-01-01",
        "dateTo": "2017-12-31",
        "sortBy": "pageviews"
    }
    assert definition.raw == expected_result


def test_inject_suite_id(fix_report_definition):
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition.inject_suite_id(fix_report_definition, "my_suite_id")
    assert definition["reportSuiteID"] == "my_suite_id"


def test_granulairty_positive():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        last_days=7,
        granularity="week"
    )
    definition._validate_granularity()


def test_granulairty_negative():
    from adobe_analytics.reports.report_definition import ReportDefinition

    definition = ReportDefinition(
        metrics="pageviews",
        dimensions="page",
        last_days=7,
        granularity="days"
    )
    with pytest.raises(AssertionError):
        definition._validate_granularity()


def test_date_days_ago():
    from adobe_analytics.reports.report_definition import ReportDefinition
    import datetime

    result = ReportDefinition._date_days_ago(4)

    expected_date = datetime.date.today() - datetime.timedelta(4)
    assert expected_date.isoformat() == result


def test_clean_field_str():
    from adobe_analytics.reports.report_definition import ReportDefinition

    result = ReportDefinition._clean_field("pageviews")
    assert result == {"id": "pageviews"}


def test_clean_field_dict():
    from adobe_analytics.reports.report_definition import ReportDefinition

    entry = {"id": "product", "classification": "Product Name"}
    result = ReportDefinition._clean_field(entry)
    assert result == entry


def test_clean_field_list():
    from adobe_analytics.reports.report_definition import ReportDefinition

    with pytest.raises(ValueError):
        ReportDefinition._clean_field(["pageviews"])


def test_suite_id_is_none_after_injection(fix_report_definition):
    # suite id in raw isn't allowed to change when calling inject_suite_id
    # this is critical, as raw returns a dict which is mutable by nature
    assert fix_report_definition.raw["reportSuiteID"] is None
    fix_report_definition.inject_suite_id("my_suite_id")
    assert fix_report_definition.raw["reportSuiteID"] is None
