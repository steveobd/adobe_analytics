from __future__ import absolute_import
from __future__ import print_function

import functools

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Suite(object):
    def __init__(self, name, suite_id, client):
        self.name = name
        self.id = suite_id
        self.client = client

    @classmethod
    def from_dict(cls, suite, client):
        return cls(name=suite['site_title'], suite_id=suite['rsid'], client=client)

    @functools.lru_cache(maxsize=None)
    def metrics(self):
        response = self.client.request(
            api='Report',
            method='GetMetrics',
            query={
                "reportSuiteID": self.id
            }
        )
        return self._response_to_dict(response)

    @functools.lru_cache(maxsize=None)
    def dimensions(self):
        response = self.client.request(
            api='Report',
            method='GetElements',
            query={
                "reportSuiteID": self.id
            }
        )
        return self._response_to_dict(response)

    @functools.lru_cache(maxsize=None)
    def segments(self):
        response = self.client.request(
            api='Segments',
            method='Get',
            query={
                "accessLevel": "shared"
            }
        )
        return self._response_to_dict(response)

    @staticmethod
    def _response_to_dict(data):
        return {item["id"]: item for item in data}

    def __repr__(self):
        return "{name} ({id})".format(id=self.id, name=self.name)
