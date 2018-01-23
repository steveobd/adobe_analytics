import pandas as pd
import numpy as np
import json

from tests import fix_report  # import is used
from tests import mock_dir


def test_classification_or_name_with_classification():
    from adobe_analytics.report import Report

    obj = {
        "name": "Product",
        "classification": "Product Name"
    }
    assert Report._classification_or_name(obj) == "Product Name"


def test_classification_or_name_without_classification():
    from adobe_analytics.report import Report

    obj = {
        "name": "Product",
    }
    assert Report._classification_or_name(obj) == "Product"


def test_fix_header_with_granularity():
    from adobe_analytics.report import Report

    data = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    result = Report._fix_header(
        dimensions=["product"],
        metrics=["pageviews"],
        data=data
    )
    assert result == ["Granularity", "product", "pageviews"]


def test_fix_header_without_granularity():
    from adobe_analytics.report import Report

    data = [
        [1, 2],
        [4, 5]
    ]
    result = Report._fix_header(
        dimensions=["product"],
        metrics=["pageviews"],
        data=data
    )
    assert result == ["product", "pageviews"]


def test_parse_data_1dim(fix_report):
    file_path = mock_dir+"/report_data_1dim.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        [np.nan, "383420", "1471063"],
        ["11911", "4", "6"]
    ]
    assert fix_report._parse_data(raw_data, 2) == result


def test_parse_data_2dim(fix_report):
    file_path = mock_dir + "/report_data_2dim.json"
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
    assert fix_report._parse_data(raw_data, 2) == result


def test_parse_data_1dim_and_granularity(fix_report):
    file_path = mock_dir + "/report_data_1dim_and_granularity.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        ["Week 35, 2017", np.nan, "102095", "24932"],
        ["Week 35, 2017", "page1", "2430", "1535"],
        ["Week 35, 2017", "page2", "2741", "1701"],
        ["Week 36, 2017", np.nan, "402268", "105046"],
        ["Week 36, 2017", "page1", "9717", "6239"],
        ["Week 36, 2017", "page3", "10550", "6799"]
    ]
    assert fix_report._parse_data(raw_data, 2) == result


def test_parse_data_2dim_and_granularity(fix_report):
    file_path = mock_dir + "/report_data_2dim_and_granularity.json"
    with open(file_path, mode="r") as json_file:
        raw_data = json.load(json_file)

    result = [
        ["Week 35, 2017", np.nan, np.nan, "102095", "24932"],
        ["Week 35, 2017", "product1", "page1", "1", "1"],
        ["Week 35, 2017", "product1", "page2", "2", "2"],
        ["Week 35, 2017", "product2", "page3", "2430", "1535"],
        ["Week 35, 2017", "product2", "page4", "2741", "1701"],
        ["Week 36, 2017", np.nan, np.nan, "402268", "105046"],
        ["Week 36, 2017", "product1", "page5", "12", "12"],
        ["Week 36, 2017", "product1", "page6", "2", "2"],
        ["Week 36, 2017", "product1", "page7", "8", "7"],
        ["Week 36, 2017", "product2", "page8", "9717", "6239"],
        ["Week 36, 2017", "product2", "page9", "10550", "6799"]
    ]
    assert fix_report._parse_data(raw_data, 2) == result


def test_parse_response_2dim(fix_report):
    file_path = mock_dir + "/Report.Get.Ready.json"
    with open(file_path, mode="r") as json_file:
        raw_response = json.load(json_file)

    fix_report.raw_response = raw_response
    fix_report.parse()

    result = pd.DataFrame([
        [np.nan, np.nan, "209726", "0"],
        [np.nan, "page1", "2", "2"],
        [np.nan, "page2", "2", "2"],
        [np.nan, "page3", "4", "8"],
        ["11911", "page4", "1", "1"],
        ["11911", "page5", "4", "5"],
        ["12900", "page6", "1", "1"]
    ], columns=["Unit Name", "Page", "Visits", "Page Views"])
    assert fix_report.dataframe.values.tolist() == result.values.tolist()
    assert list(fix_report.dataframe.columns) == list(result.columns)
