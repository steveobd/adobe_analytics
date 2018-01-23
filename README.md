# Adobe Analytics
[![Build Status](https://travis-ci.org/SaturnFromTitan/adobe_analytics.svg?branch=master)](https://travis-ci.org/SaturnFromTitan/adobe_analytics)
[![codecov](https://codecov.io/gh/SaturnFromTitan/adobe_analytics/branch/master/graph/badge.svg)](https://codecov.io/gh/SaturnFromTitan/adobe_analytics)

## Description
`adobe_analytics` is a wrapper around the Adobe Analytics REST API.

It is not meant to be comprehensive. Instead, it provides a high-level interface
to many of the common reporting queries, and allows you to do construct other queries
closer to the metal.

## Installation
Through PyPI:

    pip install adobbe_analytics

Please use pip+git in the meantime:

    pip install git+http://github.com/SaturnFromTitan/adobe_analytics.git

I developed everything in Python 3.6.0 and didn't check compatability with other versions yet.

## Authentication

The most straightforward way to authenticate is with:

```python
from adobe_analytics import Client
client = Client('my_username', 'my_password')
```

To avoid hard-coding passwords you can put your username and password
in a json file.

```bash
{
    "username": "your_aa_user_name",
    "password": "your_aa_password"
}
``` 

you can then also just pass the path for authentication
```python
from adobe_analytics import Client
client = Client.from_json("my_path")
```

## Account and suites

You can very easily access some basic information about your account and your
reporting suites (note that the result of those methods is cached, i.e. they
are available without additional API calls after the first execution):

```python
print(client.suites())
suite = client.suites()['report_suite_id']
print(suite)
print(suite.metrics())
print(suite.elements())
print(suite.segments())
```

## Running a report

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
it supports **kwargs arguments. Therefore you can specify every field that is listed in the [official Adobe Analytics](https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescription-1#reference_9ECD594AEDD240D7A475868824079F06)
documentation and supported by the REST API. However, you can also just pass a dictionary to download_report.

The fields for dimensions, metrics and segments should be lists of strings representing the ids. However, string inputs
for singular values are also supported. For a full list of available entries, refer to `suite.dimensions()`,
`suite.metrics()` and `suite.segments()` from above. Like you can see in the [documentation](https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionelement#reference_9ECD594AEDD240D7A475868824079F06)
there are even more options per dimension available. Make sure to especially check out `top` as you otherwise only
receive max. 5 entries per dimension in your report.   

## Using the Results of a report
Reports are returned as [pandas](https://github.com/pandas-dev/pandas).DataFrame. Reports as pure python, i.e. as
nested lists, are currently not supported. If that's a requirement for you, feel free to file an issue or pull request.

### Running multiple reports
If you're interested in automating a large number of reports, you can speed up the execution by first queueing all
the reports and only _then_ waiting on the results.
 
To do so, use `suite.queue_report` instead of `suite.download_report`. This method returns a `Report` object with
an updated `report.id` field. You can use this number _after_ queuing all reports in `suite.download_report`.

### Making other API requests
If you need to make other API requests you can do so by calling `client.request(api, method, data)` For example if you
wanted to call Company.GetReportSuites you would do

```python
response = client.request('Company', 'GetReportSuites')
```

### Prospect
Take a look at the issues concerning next updates. My main contribution so far is a complete redesign of this framework
and introducing higher code quality standards. While doing this I removed some features that were previously available - 
some of which I will bring back later.

Here's a small overview of features I will work on next:
- reviving test suite to ensure stability and flexibility
- distribute to pip
- data warehouse support (the parser does it already, but I need some extra logic for multi-page requests)
- error handling
- revive logging
- ensure python2.7 support
- easy interface for classification uploads

#### Tests
I am migrating the testing suite to [py.test](https://github.com/pytest-dev/pytest) right now. Execute them in
the terminal via
```bash
pytest -v
```

#### Contributers
I took over [this branch](https://github.com/dancingcactus/python-omniture) as the project there
seems to be abandoned. Thanks to everyone who put work into this project!

Special thanks go to
- [debrouwere](https://github.com/debrouwere) for initiating the framework
- [dancingcactus](https://github.com/dancingcactus) for major improvements when taking it over from debrouwere
  
