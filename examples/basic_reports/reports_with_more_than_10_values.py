from adobe_analytics import Client, ReportDefinition

client = Client.from_json("my_credentials.json")
suites = client.suites()
suite = suites["my_report_suite_id"]

# similar to classification reports you need to specify an additional parameter per dimension to receive more than
# 10 values.
# The 'top' parameter supports values up to 50k. If you need more values, you need to switch to utilize the warehouse
report_definition = ReportDefinition(
    dimensions=[
        {"id": "page", "top": 5000}
    ],
    metrics="pageviews",
    date_from="2017-01-01",
    date_to="2017-12-31"
)
dataframe = suite.download(report_definition)
print(dataframe.head())
