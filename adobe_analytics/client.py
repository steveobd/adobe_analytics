import requests
import binascii
import uuid
import hashlib
import json
from datetime import datetime

from adobe_analytics.suite import Suite


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Client(object):
    DEFAULT_ENDPOINT = 'https://api.omniture.com/admin/1.4/rest/'

    def __init__(self, username, password, endpoint=DEFAULT_ENDPOINT):
        self.username = username
        self.password = password
        self.endpoint = endpoint

        self.suites = self.report_suites()

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, mode="r") as json_file:
            credentials = json.load(json_file)
        return cls(credentials["username"], credentials["password"])

    def report_suites(self):
        response = self.request('Company', 'GetReportSuites')
        suites = [Suite.from_dict(suite, self) for suite in response['report_suites']]
        return {suite.id: suite for suite in suites}

    def request(self, api, method, query=None):
        """ Compare with https://marketing.adobe.com/developer/api-explorer """
        api_method = '{0}.{1}'.format(api, method)
        query = query or dict()

        response = requests.post(
            self.endpoint,
            params={'method': api_method},
            data=json.dumps(query),
            headers=self._build_headers()
        )
        return response.json()

    def _build_headers(self):
        nonce = str(uuid.uuid4())
        base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
        created_date = datetime.utcnow().isoformat() + 'Z'
        sha = nonce + created_date + self.password
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

    def __repr__(self):
        return "User: {0}\nReport Suites: {1}\nEndpoint: {2}"\
                .format(self.username, len(self.suites), self.endpoint)

    @staticmethod
    def _serialize_header(properties):
        header = ['{key}="{value}"'.format(key=k, value=v) for k, v in properties.items()]
        return ', '.join(header)


if __name__ == '__main__':
    from adobe_analytics import credentials_path
    from adobe_analytics import Client
    import requests_mock
    from tests import initiate_base_mock_responses, test_suite_id

    with requests_mock.mock() as m:
        initiate_base_mock_responses(mock_context=m)

        client = Client.from_json(file_path=credentials_path)
        suite = client.suites[test_suite_id]
        print(type(suite.metrics()))
        print(type(suite.dimensions()))
        print(type(suite.segments()))
