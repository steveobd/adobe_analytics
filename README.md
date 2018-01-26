# Adobe Analytics
[![Build Status](https://travis-ci.org/SaturnFromTitan/adobe_analytics.svg?branch=master)](https://travis-ci.org/SaturnFromTitan/adobe_analytics)
[![codecov](https://codecov.io/gh/SaturnFromTitan/adobe_analytics/branch/master/graph/badge.svg)](https://codecov.io/gh/SaturnFromTitan/adobe_analytics)

## Description
`adobe_analytics` is a wrapper around Adobe Analytics' REST API v1.4. It's the most advanced and stable client currently
available for Python.

It is not meant to be comprehensive. Instead, it provides a high-level interface
to many of the common reporting queries, and allows you to do construct other queries
closer to the metal.

## Installation
Through PyPI:

    pip install adobe_analytics

or via git:

    pip install git+http://github.com/SaturnFromTitan/adobe_analytics.git

Currently only Python 3.5 and 3.6 are supported.

## Examples
Please check out the code snippets in the folder `examples`. They showcase common use cases and should give you a
pretty clear understanding of how to use this framework.

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
