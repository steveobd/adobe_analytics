# Examples
Here are some basic examples to better understand the current capabilities of the framework.

Please let me know if you think something is missing or not clear. Thanks


## Authentication
Authenticating with the the API requires knowing your user name and shared secret. Both can be
obtained from the admin panel under `User Management -> Users -> Access` where Web Service Access
is granted.

When you have those, you can authenticate by using a `Client` object as follows:

```python
from adobe_analytics import Client
client = Client('my_username', 'my_password')
```

To avoid hard-coding passwords you can for instance put your username and password
in a json file similar to

```bash
{
    "username": "my_username",
    "password": "my_password"
}
``` 

In this case you can also just pass the path for authentication
```python
from adobe_analytics import Client
client = Client.from_json("my_path")
```

## Client and suites

You can very easily access some basic information about your account and your
reporting suites (note that the result of those methods is cached, i.e. they
are available without additional API calls after first execution):

```python
print(client.suites())
suite = client.suites()['report_suite_id']
print(suite)
print(suite.metrics())
print(suite.elements())
print(suite.segments())
```

## Reports

`adobbe_analytics` can run ranked, trended and over time reports. Here's a quick example:

```python
from adobe_analytics import ReportDefinition

report_def = ReportDefinition(
    dimensions="page",
    metrics="pageviews",
    last_days=1
)
report = suite.download(report_def)
```
This will generate the report definition, run the report, download and parse it for you. Alternatively you can also 
just queue the report and download it later (-> async reporting). The report definition object is very versatile as
it supports the **kwargs argument. Therefore you can specify every field that is listed in the [official Adobe Analytics
documentation](https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescription-1#reference_9ECD594AEDD240D7A475868824079F06)
and supported by the REST API.

Note that `suite.download()` also accepts queued report_ids as input for asynchronous reporting.  

The fields for dimensions, metrics and segments should be lists of strings representing the ids. However, string inputs
for singular values are also supported. For a full list of available entries, refer to `suite.dimensions()`,
`suite.metrics()` and `suite.segments()` from above. Like you can see in the [documentation](https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionelement#reference_9ECD594AEDD240D7A475868824079F06)
there are even more options per dimension available. Make sure to especially check out `top` as you otherwise only
receive max. 10 entries per dimension in your report.

To download classifciation reports, you need to specify the `classification` parameter as follows:
```python
dimensions = [{
    "id": "product",
    "classification": "Product Name"
}]
```

### Using the Results of a report
Reports are returned as [pandas](https://github.com/pandas-dev/pandas).DataFrame. Reports as pure python, i.e. as
nested lists, are currently not supported. Let me know if that's a requirement for you or file a pull request.

### Data Warehouse
Data Warehouse reports are supported since v1.0.0. To use them specify the `source` field when initiating your
`ReportDefinition` object and set its value to `warehouse`. See

```python
report_def = ReportDefinition(
    dimensions="page",
    metrics="pageviews",
    last_days=1,
    source="warehouse"
)
```
Note that those reports are less restricted, but can take much longer to download.

### Running multiple reports in parallel
If you're interested in automating a large number of reports, you can speed up the execution by first queueing all
the reports and only _then_ waiting on the results.
 
To do so, use `suite.queue_report` instead of `suite.download_report`. This method returns a `Report` object with
an updated `report.id` field. You can use this number _after_ queuing all reports in `suite.download_report`.

## Making other API requests
If you need to make other API requests you can do so by calling `client.request(api, method, data)` For example if you
wanted to call Company.GetReportSuites you would do

```python
response = client.request('Company', 'GetReportSuites')
```
