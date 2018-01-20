#!/usr/bin/python
import adobe_analytics

from tests import test_report_suite
from tests import fix_client  # this statement is used


def test_suites_is_addressable_list(fix_client):
    assert isinstance(fix_client.suites, adobe_analytics.utils.AddressableList)


def test_suite_is_suite(fix_client):
    suite = fix_client.suites[test_report_suite]
    assert isinstance(suite, adobe_analytics.suite.Suite)


def test_requests(fix_client):
    urls = [
        "https://api.omniture.com/admin/1.4/rest/",
        "https://api2.omniture.com/admin/1.4/rest/",
        "https://api3.omniture.com/admin/1.4/rest/",
        "https://api4.omniture.com/admin/1.4/rest/",
        "https://api5.omniture.com/admin/1.4/rest/"
    ]
    response = fix_client.request(api="Company", method="GetEndpoint", query={"company": ""})
    assert response in urls


# class ClientTest(unittest.TestCase):
    # def test_simple_request(self):
    #     """ simplest request possible. Company.GetEndpoint is not an authenticated method """
    #     urls = ["https://api.omniture.com/admin/1.4/rest/",
    #             "https://api2.omniture.com/admin/1.4/rest/",
    #             "https://api3.omniture.com/admin/1.4/rest/",
    #             "https://api4.omniture.com/admin/1.4/rest/",
    #             "https://api5.omniture.com/admin/1.4/rest/"]
    #     self.assertIn(self.analytics.request('Company', 'GetEndpoint'), urls, "Company.GetEndpoint failed")
    #
    # def test_authenticated_request(self):
    #     """ Request that requires authentication to make sure the auth is working
    #     """
    #     reportsuites = self.analytics.request('Company','GetReportSuites')
    #     self.assertIsInstance(reportsuites, dict, "Didn't get a valid response back")
    #     self.assertIsInstance(reportsuites['report_suites'], list, "Response doesn't contain the list of report suites might be an authentication issue")
    #
    # def test_metrics(self):
    #     """ Makes sure the suite properties can get the list of metrics
    #     """
    #     self.assertIsInstance(self.analytics.suites[test_report_suite].metrics, adobe_analytics.utils.AddressableList)
    #
    # def test_elements(self):
    #     """ Makes sure the suite properties can get the list of elements
    #     """
    #     self.assertIsInstance(self.analytics.suites[test_report_suite].elements, adobe_analytics.utils.AddressableList)
    #
    # def test_basic_report(self):
    #     """ Make sure a basic report can be run
    #     """
    #     report = self.analytics.suites[test_report_suite].report
    #     queue = []
    #     queue.append(report)
    #     response = adobe_analytics.sync(queue)
    #     self.assertIsInstance(response, list)
    #
    # def test_json_report(self):
    #     """Make sure reports can be generated from JSON objects"""
    #     report = self.analytics.suites[test_report_suite].report\
    #         .element('page')\
    #         .metric('pageviews')\
    #         .sortBy('pageviews')\
    #         .filter("s4157_55b1ba24e4b0a477f869b912")\
    #         .range("2016-08-01","2016-08-31")\
    #         .set('sortMethod',"top")\
    #         .json()
    #     self.assertEqual(report, self.analytics.jsonReport(report).json(), "The reports aren't serializating or de-serializing correctly in JSON")
    #
    # def test_account_repr_html_(self):
    #     """Make sure the account are printing out in
    #         HTML correctly for ipython notebooks"""
    #     html = self.analytics._repr_html_()
    #     test_html = "<b>Username</b>: jgrover:Justin Grover Demo</br><b>Secret</b>: ***************</br><b>Report Suites</b>: 2</br><b>Endpoint</b>: https://api.adobe_analytics.com/admin/1.4/rest/</br>"
    #     self.assertEqual(html, test_html)
    #
    # def test_account__str__(self):
    #     """ Make sure the custom str works """
    #     mystr = self.analytics.__str__()
    #     test_str = "Analytics Account -------------\n Username:             jgrover:Justin Grover Demo \n Report Suites: 2 \n Endpoint: https://api.adobe_analyticsomniture.com/admin/1.4/rest/"
    #     self.assertEqual(mystr, test_str)
    #
    # def test_suite_repr_html_(self):
    #     """Make sure the Report Suites are printing okay for ipython notebooks """
    #     html = self.analytics.suites[0]._repr_html_()
    #     test_html = "<td>adobe_analytics.api-gateway</td><td>test_suite</td>"
    #     self.assertEqual(html, test_html)
    #
    # def test_suite__str__(self):
    #     """Make sure the str represntation is working """
    #     mystr = self.analytics.suites[0].__str__()
    #     test_str = "ID adobe_analytics.api-gateway      | Name: test_suite \n"
    #     self.assertEqual(mystr,test_str)
#
#
# if __name__ == '__main__':
#     unittest.main()
