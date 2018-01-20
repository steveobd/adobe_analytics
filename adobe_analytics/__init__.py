# encoding: utf-8
from __future__ import absolute_import
import json

from .account import Account
from .suite import Suite
from .elements import Value
from .query import Query, ReportNotSubmittedError
from .reports import InvalidReportError, Report, DataWarehouseReport
from .utils import AddressableList

__version__ = '0.0.1'


def authenticate(username=None, password=None, credentials_path=None, endpoint=Account.DEFAULT_ENDPOINT):
    assert (username and password) or credentials_path, "Please provide credentials for login."
    if credentials_path is not None:
        username, password = credentials_from_json(credentials_path)
    return Account(username, password, endpoint)


def credentials_from_json(json_path):
    with open(json_path, mode="r") as json_file:
        credentials = json.load(json_file)
    return credentials["username"], credentials["password"]


def queue(queries):
    if isinstance(queries, dict):
        queries = queries.values()

    for query in queries:
        query.queue()


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
