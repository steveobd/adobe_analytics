# Adobe Analytics
[![Build Status](https://travis-ci.org/SaturnFromTitan/adobe_analytics.svg?branch=master)](https://travis-ci.org/SaturnFromTitan/adobe_analytics)
[![codecov](https://codecov.io/gh/SaturnFromTitan/adobe_analytics/branch/master/graph/badge.svg)](https://codecov.io/gh/SaturnFromTitan/adobe_analytics)

## Description
`adobe_analytics` is a wrapper around Adobe Analytics' REST API v1.4. It's the most
advanced and stable client library currently available for Python.

It provides a high-level interfaces for reporting queries (including Data Warehouse
requests) and classification uploads. It also provides an easy interface closer to
the metal for other requests to their API.

## Installation
Through PyPI:

    pip install adobe_analytics

or via git:

    pip install git+http://github.com/SaturnFromTitan/adobe_analytics.git

Supports Python 3.5+

## Examples
Please check out the code snippets in the folder `examples`. They showcase common use
cases and should give you a pretty clear understanding of how to use this framework.

## Tests
Execute tests in the terminal via
```bash
py.test -v
```

Note that tests are automatically executed on every push via [travis-ci.org](travis-ci.org).

## Contributors
I took over [this branch](https://github.com/dancingcactus/python-omniture) as the project seems to be
abandoned there. Thanks to everyone who put work into this project!

Special thanks go to
- [debrouwere](https://github.com/debrouwere) for initiating the framework
- [dancingcactus](https://github.com/dancingcactus) for major improvements when taking it over from debrouwere
