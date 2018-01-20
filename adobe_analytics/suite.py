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
    def __init__(self, title, id, account, cache=False):
        self.log = logging.getLogger(__name__)
        super(Suite, self).__init__(title, id, account)
        self.account = account

    def request(self, api, method, query={}):
        raw_query = {}
        raw_query.update(query)
        if method == 'GetMetrics' or method == 'GetElements':
            raw_query['reportSuiteID'] = self.id

        return self.account.request(api, method, raw_query)

    @property
    @utils.memoize
    def metrics(self):
        """ Return the list of valid metricsfor the current report suite"""
        if self.account.cache:
            data = self.request_cache('Report', 'GetMetrics')
        else:
            data = self.request('Report', 'GetMetrics')
        return Value.list('metrics', data, self, 'name', 'id')

    @property
    @utils.memoize
    def elements(self):
        """ Return the list of valid elementsfor the current report suite """
        if self.account.cache:
            data = self.request_cached('Report', 'GetElements')
        else:
            data = self.request('Report', 'GetElements')
        return Value.list('elements', data, self, 'name', 'id')

    @property
    @utils.memoize
    def segments(self):
        """ Return the list of valid segments for the current report suite """
        if self.account.cache:
            data = self.request_cached('Segments', 'Get',{"accessLevel":"shared"})
        else:
            data = self.request('Segments', 'Get',{"accessLevel":"shared"})
        return Value.list('segments', data, self, 'name', 'id',)

    @property
    def report(self):
        """ Return a report to be run on this report suite """
        return Query(self)

    def jsonReport(self,reportJSON):
        """Creates a report from JSON. Accepts either JSON or a string. Useful for deserializing requests"""
        q = Query(self)
        #TODO: Add a method to the Account Object to populate the report suite this call will ignore it on purpose
        if type(reportJSON) == str:
            reportJSON = json.loads(reportJSON)

        reportJSON = reportJSON['reportDescription']

        if 'dateFrom' in reportJSON and 'dateTo' in reportJSON:
            q = q.range(reportJSON['dateFrom'],reportJSON['dateTo'])
        elif 'dateFrom' in reportJSON:
            q = q.range(reportJSON['dateFrom'])
        elif 'date' in reportJSON:
            q = q.range(reportJSON['date'])
        else:
            q = q

        if 'dateGranularity' in reportJSON:
            q = q.granularity(reportJSON['dateGranularity'])

        if 'source' in reportJSON:
            q = q.set('source',reportJSON['source'])

        if 'metrics' in reportJSON:
            for m in reportJSON['metrics']:
                q = q.metric(m['id'])

        if 'elements' in reportJSON:
            for e in reportJSON['elements']:
                id = e['id']
                del e['id']
                q= q.element(id, **e)

        if 'locale' in reportJSON:
            q = q.set('locale',reportJSON['locale'])

        if 'sortMethod' in reportJSON:
            q = q.set('sortMethod',reportJSON['sortMethod'])

        if 'sortBy' in reportJSON:
            q = q.sortBy(reportJSON['sortBy'])

        #WARNING This doesn't carry over segment IDs meaning you can't manipulate the segments in the new object
        #TODO Loop through and add segment ID with filter method (need to figure out how to handle combined)
        if 'segments' in reportJSON:
            q = q.set('segments', reportJSON['segments'])

        if 'anomalyDetection' in reportJSON:
            q = q.set('anomalyDetection',reportJSON['anomalyDetection'])

        if 'currentData' in reportJSON:
            q = q.set('currentData',reportJSON['currentData'])

        if 'elementDataEncoding' in reportJSON:
            q = q.set('elementDataEncoding',reportJSON['elementDataEncoding'])
        return q

    def _repr_html_(self):
        """ Format in HTML for iPython Users """
        return "<td>{0}</td><td>{1}</td>".format(self.id, self.title)

    def __str__(self):
        return "ID {0:25} | Name: {1} \n".format(self.id, self.title)