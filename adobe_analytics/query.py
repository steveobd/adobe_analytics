# encoding: utf-8
from __future__ import absolute_import
from __future__ import print_function

import time
from copy import copy
import json
import logging
import sys

from . import reports


class Query(object):
    GRANULARITY_LEVELS = ['hour', 'day', 'week', 'month', 'quarter', 'year']
    STATUSES = ["Not Submitted", "Not Ready", "Done"]

    def __init__(self, suite):
        """ Setup the basic structure of the report query. """
        self.log = logging.getLogger(__name__)
        self.suite = suite
        self.raw = {}

        #Put the report suite in so the user can print
        #the raw query and have it work as is
        self.raw['reportSuiteID'] = str(self.suite.id)
        self.id = None
        self.method = "Get"
        self.status = self.STATUSES[0]

        #The report object
        self.report = reports.Report

        #The fully hydrated report object
        self.processed_response = None
        self.unprocessed_response = None

    def _normalize_value(self, value, category):
        if isinstance(value, Element):
            return value
        else:
            return getattr(self.suite, category)[value]

    def _serialize_value(self, value, category):
        return self._normalize_value(value, category).serialize()

    def _serialize_values(self, values, category):
        if not isinstance(values, list):
            values = [values]

        return [self._serialize_value(value, category) for value in values]

    def _serialize(self, obj):
        if isinstance(obj, list):
            return [self._serialize(el) for el in obj]
        elif isinstance(obj, Element):
            return obj.serialize()
        else:
            return obj

    def clone(self):
        """ Return a copy of the current object. """
        query = Query(self.suite)
        query.raw = copy(self.raw)
        query.report = self.report
        query.status = self.status
        query.processed_response = self.processed_response
        query.unprocessed_response = self.unprocessed_response
        return query

    def build(self):
        """ Return the report descriptoin as an object """
        return {'reportDescription': self.raw}

    def queue(self):
        """ Submits the report to the Queue on the Adobe side. """
        q = self.build()
        self.log.debug("Suite Object: %s  Method: %s, Query %s",
                       self.suite, self.report.method, q)
        self.id = self.suite.request('Report',
                                     self.report.method,
                                     q)['reportID']
        self.status = self.STATUSES[1]
        return self

    def probe(self, heartbeat=None, interval=1, soak=False):
        """ Keep checking until the report is done"""
        #Loop until the report is done
        while self.is_ready() == False:
            if heartbeat:
                heartbeat()
            time.sleep(interval)
            #Use a back off up to 30 seconds to play nice with the APIs
            if interval < 1:
                interval = 1
            elif interval < 30:
                interval = round(interval * 1.5)
            else:
                interval = 30
            self.log.debug("Check Interval: %s seconds", interval)
            
    def is_ready(self):
        """ inspects the response to see if the report is ready """
        if self.status == self.STATUSES[0]:
            raise ReportNotSubmittedError('{"message":"Doh! the report needs to be submitted first"}')
        elif self.status == self.STATUSES[1]:
            try:
                # the request method catches the report and populates it automatically
                response = self.suite.request('Report','Get',{'reportID': self.id})
                self.status = self.STATUSES[2]
                self.unprocessed_response = response
                self.processed_response = self.report(response, self)
                return True
            except reports.ReportNotReadyError:
                self.status = self.STATUSES[1]
                #raise reports.InvalidReportError(response)
                return False
        elif self.status == self.STATUSES[2]:
            return True

    def sync(self, heartbeat=None, interval=0.01):
        """ Run the report synchronously,"""
        if self.status == self.STATUSES[0]:
            self.queue()
            self.probe(heartbeat, interval)
        if self.status == self.STATUSES[1]:
            self.probe()
        return self.processed_response

    def async(self, callback=None, heartbeat=None, interval=1):
        """ Run the Report Asynchrnously """
        if self.status == self.STATUSES[0]:
            self.queue()
        return self
        
    def get_report(self):
        self.is_ready()
        if self.status == self.STATUSES[2]:
            return self.processed_response
        else:
            raise reports.ReportNotReadyError('{"message":"Doh! the report is not ready yet"}')
        
    def run(self, defaultheartbeat=True, heartbeat=None, interval=0.01):
        """Shortcut for sync(). Runs the current report synchronously. """
        if defaultheartbeat == True:
            rheartbeat = self.heartbeat
        else:
            rheartbeat = heartbeat

        return self.sync(rheartbeat, interval)

    def heartbeat(self):
        """ A default heartbeat method that prints a dot for each request """
        sys.stdout.write('.')
        sys.stdout.flush()

    def check(self):
        """
            Basically an alias to is ready to make the interface a bit better
        """
        return self.is_ready()

    def cancel(self):
        """ Cancels a the report from the Queue on the Adobe side. """
        return self.suite.request('Report', 'CancelReport', {'reportID': self.id})

    def json(self):
        """ Return a JSON string of the Request """
        return str(json.dumps(self.build(), indent=4, separators=(',', ': '), sort_keys=True))

    def __str__(self):
        return self.json()
