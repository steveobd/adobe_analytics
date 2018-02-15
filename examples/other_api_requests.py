"""
The client class has a request method that allows all sorts of generic API requests to Adobe's v1.4 REST API.

To get a comprehensive overview of available APIs and methods check out the official Adobe Analytics API Explorer:
https://marketing.adobe.com/developer/api-explorer
"""
from adobe_analytics import Client

client = Client.from_json("my_path.json")

# The request below returns a list of all evars available in all specified report suites.
result = client.request(
    api="ReportSuite",
    method="GetEvars",
    data={
        "rsid_list": [
            "my_report_suite_id_1",
            "my_report_suite_id_2",
            "...",
            "my_report_suite_id_n"
        ]
    }
)
print(result)
