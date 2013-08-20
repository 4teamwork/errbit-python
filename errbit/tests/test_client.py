from errbit.client import Client
from unittest2 import TestCase
import os
import pkg_resources


ERRBIT_VERSION = pkg_resources.require('errbit')[0].version
REQUESTS_VERSION = pkg_resources.require('requests')[0].version


class TestClient(TestCase):

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
             'version': ERRBIT_VERSION},

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
             'version': REQUESTS_VERSION},

            client.get_notifier())
