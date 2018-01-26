"""
Queuing a report requests the data without blocking the program.

While waiting for your report your program can do other things - for instance requesting more reports ;)
This is handy for instance when you want to pull a report for multiple report suites.

Also note that a report definition is independent of a Suite.
"""
import pandas as pd
from adobe_analytics import Client, ReportDefinition

client = Client.from_json("my_credentials.json")
report_definition = ReportDefinition(
    dimensions="page",
    metrics="pageviews",
    date_from="2017-01-01",
    date_to="2017-12-31"
)
report_ids = dict()

# request report per suite
suites = client.suites()
for suite_id, suite in suites.items():
    report_id = suite.queue(report_definition)
    report_ids[suite_id] = report_id

# download data
reports = list()
for suite_id, report_id in report_ids.items():
    suite = suites[suite_id]

    report = suite.download(report_id)
    report.insert(0, "SuideID", suite_id)  # to identify which row belongs to which reporting suite
    reports.append(report)

df = pd.concat(reports, ignore_index=True)
print(df.head())
