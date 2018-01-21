# encoding: utf-8
from __future__ import absolute_import, print_function
import os


__version__ = '0.0.1'
app_dir = os.path.dirname(__file__)
app_dir_components = app_dir.split(os.sep)
base_dir = os.sep.join(app_dir_components[:-1])
credentials_path = base_dir+"/aa_credentials.json"

from adobe_analytics.client import Client
from adobe_analytics.suite import Suite
from adobe_analytics.query import Query, ReportNotSubmittedError


def queue(queries):
    if isinstance(queries, dict):
        queries = queries.values()

    for q in queries:
        q.queue()


def sync(queries, heartbeat=None, interval=1):
    """
    `will queue a number of reports and then
    block until the results are all ready.

    Queueing reports is idempotent, meaning that you can also
    use `adobe_analytics.sync` to fetch the results for queries that
    have already been queued:

        query = suite.report \
            .range('2013-06-06')
            .over_time('pageviews', 'page')
        adobe_analytics.queue(query)
        adobe_analytics.sync(query)

    The interval will operate under an exponential decay until it reaches 5 minutes.
    At which point it will ping every 5 minutes
    """
    queue(queries)

    if isinstance(queries, list):
        return [query.sync(heartbeat, interval) for query in queries]
    elif isinstance(queries, dict):
        return {key: query.sync(heartbeat, interval) for key, query in queries.items()}
    else:
        message = "Queries should be a list or a dictionary, received: {}".format(
            queries.__class__)
        raise ValueError(message)
