from __future__ import absolute_import
from __future__ import print_function

import json
import logging

from .elements import Value
from .query import Query
from . import utils

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Suite(Value):
    """Lets you query a specific report suite. """
    def __init__(self, title, suite_id, client):
        self.log = logging.getLogger(__name__)
        super(Suite, self).__init__(title, suite_id, client)
        self.client = client

    @classmethod
    def from_dict(cls, suite, client):
        return cls(title=suite['site_title'], suite_id=suite['rsid'], client=client)

    def request(self, api, method, query={}):
        raw_query = {}
        raw_query.update(query)
        if method in ['GetMetrics', 'GetElements']:
            raw_query['reportSuiteID'] = self.id
        return self.client.request(api, method, raw_query)

    @property
    @utils.memoize
    def metrics(self):
        """ Return the list of valid metricsfor the current report suite"""
        if self.client.cache:
            data = self.request_cache('Report', 'GetMetrics')
        else:
            data = self.request('Report', 'GetMetrics')
        return Value.list('metrics', data, self, 'name', 'id')

    @property
    @utils.memoize
    def elements(self):
        """ Return the list of valid elementsfor the current report suite """
        if self.client.cache:
            data = self.request_cached('Report', 'GetElements')
        else:
            data = self.request('Report', 'GetElements')
        return Value.list('elements', data, self, 'name', 'id')

    @property
    @utils.memoize
    def segments(self):
        """ Return the list of valid segments for the current report suite """
        if self.client.cache:
            data = self.request_cached('Segments', 'Get',{"accessLevel":"shared"})
        else:
            data = self.request('Segments', 'Get',{"accessLevel":"shared"})
        return Value.list('segments', data, self, 'name', 'id',)

    @property
    def report(self):
        """ Return a report to be run on this report suite """
        return Query(self)

    def jsonReport(self, report_json):
        """Creates a report from JSON. Accepts either JSON or a string. Useful for deserializing requests"""
        q = Query(self)

        # TODO: Add a method to the Account Object to populate the report suite this call will ignore it on purpose
        if type(report_json) == str:
            report_json = json.loads(report_json)

        report_json = report_json['reportDescription']

        if 'dateFrom' in report_json and 'dateTo' in report_json:
            q = q.range(report_json['dateFrom'], report_json['dateTo'])
        elif 'dateFrom' in report_json:
            q = q.range(report_json['dateFrom'])
        elif 'date' in report_json:
            q = q.range(report_json['date'])
        else:
            q = q

        if 'dateGranularity' in report_json:
            q = q.granularity(report_json['dateGranularity'])

        if 'source' in report_json:
            q = q.set('source', report_json['source'])

        if 'metrics' in report_json:
            for m in report_json['metrics']:
                q = q.metric(m['id'])

        if 'elements' in report_json:
            for e in report_json['elements']:
                id = e['id']
                del e['id']
                q= q.element(id, **e)

        if 'locale' in report_json:
            q = q.set('locale', report_json['locale'])

        if 'sortMethod' in report_json:
            q = q.set('sortMethod', report_json['sortMethod'])

        if 'sortBy' in report_json:
            q = q.sortBy(report_json['sortBy'])

        # WARNING This doesn't carry over segment IDs meaning you can't manipulate the segments in the new object
        # TODO Loop through and add segment ID with filter method (need to figure out how to handle combined)
        if 'segments' in report_json:
            q = q.set('segments', report_json['segments'])

        if 'anomalyDetection' in report_json:
            q = q.set('anomalyDetection', report_json['anomalyDetection'])

        if 'currentData' in report_json:
            q = q.set('currentData', report_json['currentData'])

        if 'elementDataEncoding' in report_json:
            q = q.set('elementDataEncoding', report_json['elementDataEncoding'])
        return q

    def _repr_html_(self):
        """ Format in HTML for iPython Users """
        return "<td>{0}</td><td>{1}</td>".format(self.id, self.title)

    def __str__(self):
        return "ID {0:25} | Name: {1} \n".format(self.id, self.title)
