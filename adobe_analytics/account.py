from __future__ import absolute_import
from __future__ import print_function

import requests
import binascii
from datetime import datetime, date
import logging
import uuid
import hashlib
import base64
import os
import json
import logging.config
import io

from . import reports
from . import utils
from .suite import Suite


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration.  """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with io.open(path, 'rt') as f:
            config = json.load(f)
        f.close()
        logging.config.dictConfig(config)
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    else:
        logging.basicConfig(level=default_level)


class Account(object):
    DEFAULT_ENDPOINT = 'https://api.adobe_analyticsomniture.com/amin/1.4/rest/'

    def __init__(self, username, secret, endpoint, cache=False, cache_key=None):
        """Authentication to make requests."""
        setup_logging()
        self.log = logging.getLogger(__name__)
        self.log.info(datetime.now().strftime(DATETIME_FORMAT))

        self.username = username
        self.secret = secret
        self.endpoint = endpoint

        # Allow someone to set a custom cache key
        self.cache = cache
        if cache_key:
            self.cache_key = cache_key
        else:
            self.cache_key = date.today().isoformat()

        if self.cache:
            data = self.request_cached('Company', 'GetReportSuites')['report_suites']
        else:
            data = self.request('Company', 'GetReportSuites')['report_suites']
        suites = [Suite(suite['site_title'], suite['rsid'], self) for suite in data]
        self.suites = utils.AddressableList(suites)

    def request_cached(self, api, method, query={}, cache_key=None):
        if cache_key:
            key = cache_key
        else:
            key = self.cache_key

        #Generate a shortened hash of the query string so that method don't collide
        query_hash = base64.urlsafe_b64encode(hashlib.md5(query).digest())

        try:
            with open(self.file_path+'/data_'+api+'_'+method+'_'+query_hash+'_'+key+'.txt') as fp:
                for line in fp:
                    if line:
                        data = ast.literal_eval(line)

        except IOError as e:
            data = self.request(api, method, query)

            # Capture all other old text files
            #TODO decide if the query should be included in the file list to be cleared out when the cache key changes
            filelist = [f for f in os.listdir(self.file_path) if f.startswith('data_'+api+'_'+method)]

            # Delete them
            for f in filelist:
                os.remove(self.file_path+'/'+f)

            # Build the new data
            the_file = open(self.file_path+'/data_'+api+'_'+method+'_'+query_hash+'_'+key+'.txt', 'w')
            the_file.write(str(data))
            the_file.close()

    def request(self, api, method, query={}):
        """
        Make a request to the Adobe APIs.

        * api -- the class of APIs you would like to call (e.g. Report,
            ReportSuite, Company, etc.)
        * method -- the method you would like to call inside that class
            of api
        * query -- a python object representing the parameters you would
            like to pass to the API
        """
        self.log.info("Request: %s.%s  Parameters: %s", api, method, query)
        response = requests.post(
            self.endpoint,
            params={'method': api + '.' + method},
            data=json.dumps(query),
            headers=self._build_token()
            )
        self.log.debug("Response for %s.%s:%s", api, method, response.text)
        json_response = response.json()

        if type(json_response) == dict:
            self.log.debug("Error Code %s", json_response.get('error'))
            if json_response.get('error') == 'report_not_ready':
                raise reports.ReportNotReadyError(json_response)
            elif json_response.get('error') != None:
                raise reports.InvalidReportError(json_response)
            else:
                return json_response
        else:
            return json_response

    def jsonReport(self, reportJSON):
        """Generates a Report from the JSON (including selecting the report suite)"""
        if type(reportJSON) == str:
            reportJSON = json.loads(reportJSON)
        suiteID = reportJSON['reportDescription']['reportSuiteID']
        suite = self.suites[suiteID]
        return suite.jsonReport(reportJSON)

    def _serialize_header(self, properties):
        header = []
        for key, value in properties.items():
            header.append('{key}="{value}"'.format(key=key, value=value))
        return ', '.join(header)

    def _build_token(self):
        nonce = str(uuid.uuid4())
        base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
        created_date = datetime.utcnow().isoformat() + 'Z'
        sha = nonce + created_date + self.secret
        sha_object = hashlib.sha1(sha.encode())
        password_64 = binascii.b2a_base64(sha_object.digest())

        properties = {
            "Username": self.username,
            "PasswordDigest": password_64.decode().strip(),
            "Nonce": base64nonce.decode().strip(),
            "Created": created_date,
        }
        header = 'UsernameToken ' + self._serialize_header(properties)
        return {'X-WSSE': header}

    def _repr_html_(self):
        """ Format in HTML for iPython Users """
        html = ""
        html += "<b>{0}</b>: {1}</br>".format("Username", self.username)
        html += "<b>{0}</b>: {1}</br>".format("Secret", "***************")
        html += "<b>{0}</b>: {1}</br>".format("Report Suites", len(self.suites))
        html += "<b>{0}</b>: {1}</br>".format("Endpoint", self.endpoint)
        return html

    def __str__(self):
        return ("Username: {0}\n"
                "Report Suites: {1}\n"
                "Endpoint: {2}"
                .format(self.username, len(self.suites), self.endpoint))
