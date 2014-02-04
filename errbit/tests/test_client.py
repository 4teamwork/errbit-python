from errbit import httpclients
from errbit.client import Client
from mocker import MockerTestCase
import os
import pkg_resources
import sys
import threading


ERRBIT_VERSION = pkg_resources.require('errbit')[0].version
REQUESTS_VERSION = pkg_resources.require('requests')[0].version

try:
    raise AttributeError("Foo instance has no attribute 'bar'")
except:
    EXC_INFO = sys.exc_info()


class MockHTTPClient(object):

    def __init__(self):
        self.posted = []

    def __call__(self):
        return self

    def post(self, url, encoded_post_data):
        self.posted.append({'url': url,
                            'data': encoded_post_data})


class TestClient(MockerTestCase):

    def setUp(self):
        self.http_client = MockHTTPClient()
        httpclients.HTTP_CLIENTS['mock'] = self.http_client
        os.environ['ERRBIT_HTTP_CLIENT'] = 'mock'

    def tearDown(self):
        del httpclients.HTTP_CLIENTS['mock']
        for key in filter(lambda key: key.startswith('ERRBIT_'),
                          os.environ.keys()):
            del os.environ[key]

    def test_set_api_key_with_environment_variables(self):
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'
        client = Client()
        self.assertEquals('abcd1234', client.get_api_key())

    def test_configure_errbit_url_with_environment_variable(self):
        os.environ['ERRBIT_URL'] = 'http://errbit.local/api'

        client = Client()
        self.assertEquals('http://errbit.local/api', client.get_errbit_url())

    def test_posting_exception(self):
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'
        os.environ['ERRBIT_URL'] = 'http://errbit.local/api'
        request_data = {'url': 'http://foo/bar'}
        env_data = {'project-root': os.getcwd()}
        client = Client()

        xmlgenerator = self.mocker.replace('errbit.xmlgenerator.generate_xml')
        self.expect(xmlgenerator('abcd1234', client.get_notifier(),
                                 EXC_INFO, request=request_data, environment=env_data)
                    ).result('<XMLDATA/>')

        self.mocker.replay()
        client.post(EXC_INFO, request=request_data)
        while threading.active_count() > 1:
            pass

        self.assertEquals([{'data': '<XMLDATA/>', 'url': 'http://errbit.local/api'}],
                          self.http_client.posted)

    def test_client_filters_test_exception(self):
        cfg_path = os.path.join(os.path.dirname(__file__), 'assets', 'errbit_ignore.json')
        os.environ['ERRBIT_IGNORE'] = cfg_path
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'
        os.environ['ERRBIT_URL'] = 'http://errbit.local/api'

        client = Client()
        client.post(EXC_INFO, request={'url': 'http://foo/bar'})
        while threading.active_count() > 1:
            pass

        self.assertEquals(
            [],
            self.http_client.posted)

    def test_client_logs_invalid_config_file(self):
        os.environ['ERRBIT_IGNORE'] = __file__
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'

        client = Client()
        client.post(EXC_INFO, request={'url': 'http://foo/bar'})
        while threading.active_count() > 1:
            pass

        self.assertEquals(
            2,
            len(self.http_client.posted))
