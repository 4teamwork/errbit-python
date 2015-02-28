from errbit.testing import ERRBIT_PLONE_FUNCTIONAL
from ftw.testbrowser import browsing
from unittest2 import TestCase
import os


class TestRequestInfoCleanup(TestCase):
    layer = ERRBIT_PLONE_FUNCTIONAL

    envs = {
        'ERRBIT_URL': 'https://errbit.local/notifier_api/v2/notices',
        'ERRBIT_API_KEY': '123THEKEY123',
        'ERRBIT_APP_ID': '123THEID123',
        'ERRBIT_ENVIRONMENT': 'DEV'}

    def setUp(self):
        os.environ.update(self.envs)

    def tearDown(self):
        for name in self.envs.keys():
            if name in os.environ:
                del os.environ[name]

    @browsing
    def test_javascript_contains_airbrake_shim(self, browser):
        browser.open(view='errbit-plone.js')
        self.assertIn('global.Airbrake =', browser.contents)

    @browsing
    def test_contains_configuration(self, browser):
        browser.open(view='errbit-plone.js')
        last_lines = '\n'.join(browser.contents.splitlines()[-5:])
        self.assertIn('client.setProject("123THEID123", "123THEKEY123");', last_lines)
        self.assertIn('client.setHost("https://errbit.local");', last_lines)
        self.assertIn('client.setEnvironmentName("DEV");', last_lines)

    @browsing
    def test_content_type_header_is_set(self, browser):
        browser.open(view='errbit-plone.js')
        self.assertEquals('application/javascript; charset=utf-8',
                          browser.headers.get('Content-Type'))

    @browsing
    def test_empty_when_not_configured_well(self, browser):
        del os.environ['ERRBIT_APP_ID']
        browser.open(view='errbit-plone.js')
        self.assertEquals('', browser.contents)
