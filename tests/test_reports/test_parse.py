import pandas as pd
import numpy as np
import json

from tests import mock_dir
import adobe_analytics.reports.parse as parse


def test_classification_or_name_with_classification():
    obj = {
        "name": "Product",
        "classification": "Product Name"
    }
    assert parse._classification_or_name(obj) == "Product Name"


def test_classification_or_name_without_classification():
    obj = {
        "name": "Product",
    }
    assert parse._classification_or_name(obj) == "Product"


def test_fix_header_with_granularity():
    data = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    result = parse._fix_header(
        dimensions=["product"],
        metrics=["pageviews"],
        data=data
    )
    assert result == ["Datetime", "product", "pageviews"]


def test_fix_header_without_granularity():
    data = [
        [1, 2],
        [4, 5]
    ]
    result = parse._fix_header(
        dimensions=["product"],
        metrics=["pageviews"],
        data=data
    )
    assert result == ["product", "pageviews"]


def test_dim_is_nan_no_name():
    chunk = dict()
    assert parse._dimension_value_is_nan(chunk)


def test_dim_is_nan_empty_name():
    chunk = {"name": ""}
    assert parse._dimension_value_is_nan(chunk)


def test_dim_is_nan_no_name_classification():
    chunk = {"name": "::unspecified::"}
    assert parse._dimension_value_is_nan(chunk)


def test_dim_is_nan_false():
    chunk = {"name": "lasttouchchannel"}
    assert not parse._dimension_value_is_nan(chunk)


def test_parse_datetime():
    chunk = {
        "year": 2017,
        "month": 3,
        "day": 1,
        "hour": 5
    }
    assert parse._to_datetime(chunk) == "2017-03-01 05:00:00"


def test_dimension_value_nan():
    chunk = dict()
    assert pd.isnull(parse._dimension_value(chunk))


def test_dimension_value_datetime():
    chunk = {
        "name": "Mon, 1st March 2017",
        "year": 2017,
        "month": 3,
        "day": 1,
        "hour": 5
    }
    assert parse._dimension_value(chunk) == "2017-03-01 05:00:00"


def test_dimension_value_name():
    chunk = {"name": "Product Name"}
    assert parse._dimension_value(chunk) == "Product Name"


def test_parse_data_1dim():
    file_path = mock_dir+"/Report.Get-data_1dim.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        [np.nan, "383420", "1471063"],
        ["11911", "4", "6"]
    ]
    assert parse._parse_data(raw_data, 2) == result


def test_parse_data_2dim():
    file_path = mock_dir + "/Report.Get-data_2dim.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        [np.nan, np.nan, "209726", "0"],
        [np.nan, "page1", "2", "2"],
        [np.nan, "page2", "2", "2"],
        ["11911", "page3", "1", "1"],
        ["11911", "page4", "4", "5"],
        ["12900", "page5", "1", "1"]
    ]
    assert parse._parse_data(raw_data, 2) == result


def test_parse_data_1dim_and_granularity():
    file_path = mock_dir + "/Report.Get-data_1dim_and_granularity.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        ["2017-08-28 00:00:00", np.nan, "102095", "24932"],
        ["2017-08-28 00:00:00", "page1", "2430", "1535"],
        ["2017-08-28 00:00:00", "page2", "2741", "1701"],
        ["2017-09-04 00:00:00", np.nan, "402268", "105046"],
        ["2017-09-04 00:00:00", "page1", "9717", "6239"],
        ["2017-09-04 00:00:00", "page3", "10550", "6799"]
    ]
    assert parse._parse_data(raw_data, 2) == result


def test_parse_data_2dim_and_granularity():
    file_path = mock_dir + "/Report.Get-data_2dim_and_granularity.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        ["2017-08-28 00:00:00", np.nan, np.nan, "102095", "24932"],
        ["2017-08-28 00:00:00", "product1", "page1", "1", "1"],
        ["2017-08-28 00:00:00", "product1", "page2", "2", "2"],
        ["2017-08-28 00:00:00", "product2", "page3", "2430", "1535"],
        ["2017-08-28 00:00:00", "product2", "page4", "2741", "1701"],
        ["2017-09-04 00:00:00", np.nan, np.nan, "402268", "105046"],
        ["2017-09-04 00:00:00", "product1", "page5", "12", "12"],
        ["2017-09-04 00:00:00", "product1", "page6", "2", "2"],
        ["2017-09-04 00:00:00", "product1", "page7", "8", "7"],
        ["2017-09-04 00:00:00", "product2", "page8", "9717", "6239"],
        ["2017-09-04 00:00:00", "product2", "page9", "10550", "6799"]
    ]
    assert parse._parse_data(raw_data, 2) == result


def test_parse_response_2dim():
    file_path = mock_dir + "/Report.Get-2dim.json"
    with open(file_path, mode="r") as json_file:
        raw_response = json.load(json_file)
    result = parse.parse(raw_response)

    expected_result = pd.DataFrame([
        [np.nan, np.nan, "209726", "0"],
        [np.nan, "page1", "2", "2"],
        [np.nan, "page2", "2", "2"],
        [np.nan, "page3", "4", "8"],
        ["11911", "page4", "1", "1"],
        ["11911", "page5", "4", "5"],
        ["12900", "page6", "1", "1"]
    ], columns=["Unit Name", "Page", "Visits", "Page Views"])
    assert result.values.tolist() == expected_result.values.tolist()
    assert list(result.columns) == list(expected_result.columns)


def test_parse_response_2dim_and_granularity_missing_values():
    file_path = mock_dir + "/Report.Get-2dim_and_granularity_missing_values.json"
    with open(file_path, mode="r") as json_file:
        raw_response = json.load(json_file)
    result = parse.parse(raw_response)

    expected_result = pd.DataFrame([
        ["2018-01-01 04:00:00", np.nan, "mkt1", "31"],
        ["2018-01-01 04:00:00", np.nan, "mkt2", "30"],
        ["2018-01-01 04:00:00", "product1", "mkt1", "28"],
        ["2018-01-01 04:00:00", "product1", "mkt2", "18"],
        ["2018-01-01 04:00:00", "product2", "mkt2", "11"]
    ], columns=["Datetime", "Product Name", "Last Touch Marketing Channel", "Visits"])
    assert result.values.tolist() == expected_result.values.tolist()
    assert list(result.columns) == list(expected_result.columns)
