from errbit.client import Client
from mocker import MockerTestCase
import os
import pkg_resources
import sys


ERRBIT_VERSION = pkg_resources.require('errbit')[0].version
REQUESTS_VERSION = pkg_resources.require('requests')[0].version

try:
    raise AttributeError("Foo instance has no attribute 'bar'")
except:
    EXC_INFO = sys.exc_info()


class TestClient(MockerTestCase):

    def tearDown(self):
        for key in filter(lambda key: key.startswith('ERRBIT_'),
                          os.environ.keys()):
            del os.environ[key]

    def test_set_api_key_with_environment_variables(self):
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'
        client = Client()
        self.assertEquals('abcd1234', client.get_api_key())

    def test_notifier_defaults(self):
        client = Client()

        self.assertEquals(
            {'name': 'errbit',
             'version': ERRBIT_VERSION,
             'url': ''},

            client.get_notifier())

    def test_setting_notifier_info_with_environment_variables(self):
        os.environ['ERRBIT_NOTIFIER_NAME'] = 'my app'
        os.environ['ERRBIT_NOTIFIER_VERSION'] = '1.7'
        os.environ['ERRBIT_NOTIFIER_URL'] = 'http://my.app/'

        client = Client()
        self.assertEquals(
            {'name': 'my app',
             'version': '1.7',
             'url': 'http://my.app/'},

            client.get_notifier())

    def test_getting_notifier_info_from_package(self):
        os.environ['ERRBIT_NOTIFIER_PACKAGE'] = 'requests'

        client = Client()
        self.assertEquals(
            {'name': 'requests',
             'version': REQUESTS_VERSION,
             'url': ''},

            client.get_notifier())

    def test_configure_errbit_url_with_environment_variable(self):
        os.environ['ERRBIT_URL'] = 'http://errbit.local/api'

        client = Client()
        self.assertEquals('http://errbit.local/api', client.get_errbit_url())

    def test_posting_exception(self):
        os.environ['ERRBIT_API_KEY'] = 'abcd1234'
        os.environ['ERRBIT_URL'] = 'http://errbit.local/api'
        request_data = {'url': 'http://foo/bar'}
        env_data = {'environment-name': 'production'}
        client = Client()

        xmlgenerator = self.mocker.replace('errbit.xmlgenerator.generate_xml')
        self.expect(xmlgenerator('abcd1234', client.get_notifier(),
                                 EXC_INFO, request=request_data, environment=env_data)
                    ).result('<XMLDATA/>')

        req_class = self.mocker.replace('errbit.request.ThreadedRequest')
        req = self.mocker.mock()
        self.expect(req_class('http://errbit.local/api', '<XMLDATA/>')).result(req)
        self.expect(req.start())

        self.mocker.replay()
        client.post(EXC_INFO, request=request_data, environment=env_data)
