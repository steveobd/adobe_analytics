"""
Note that a report definition is independent of a Suite.

Often you want to download a report for multiple suites. With this helper method
first all your reports are requested and then one after another downloaded. This will
save you time as you're downloading your first reports already while the bigger ones are
still being processed.
"""
from adobe_analytics import Client, ReportDefinition
from adobe_analytics import download_async

client = Client.from_json("my_credentials.json")
report_definition = ReportDefinition(
    dimensions="page",
    metrics="pageviews",
    date_from="2017-01-01",
    date_to="2017-12-31"
)

# for maximum speed improvements sort your suite_ids list by expected size of data in response
# sort from smallest to largest
df = download_async(client, report_definition, suite_ids=["suite_id_1", "suite_id_2"])
print(df.head())
