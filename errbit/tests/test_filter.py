from errbit.client import Client
from unittest2 import TestCase
import os


class SimpleFilterTests(TestCase):

    def tearDown(self):
        for key in filter(lambda key: key.startswith('ERRBIT_'),
                          os.environ.keys()):
            del os.environ[key]

    def test_ignore_regex_without_cfg(self):
        client = Client()
        self.assertEquals(
            [],
            client.get_ignore_regex())

    def test_ignore_regex(self):
        cfg_path = os.path.join(os.path.dirname(__file__), 'assets', 'errbit_ignore.json')
        os.environ['ERRBIT_IGNORE'] = cfg_path
        client = Client()

        self.assertEquals(
            ["^AttributeError\\b", "regex2"],
            client.get_ignore_regex())
