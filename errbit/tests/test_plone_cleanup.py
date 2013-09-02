from errbit.plone.cleanup import REPLACEMENT
from errbit.plone.cleanup import cleanup_request_info
from unittest2 import TestCase


class TestRequestInfoCleanup(TestCase):

    def test_password_params_are_removed(self):
        input = {
            'params': {
                'form_password': 'foo',
                'form_password_ctl': 'bar'}}

        expected = {
            'params': {
                'form_password': REPLACEMENT,
                'form_password_ctl': REPLACEMENT}}

        self.assertEquals(expected, cleanup_request_info(input))

    def test_ac_cookie_is_removed_from_session(self):
        input = {
            'session': {
                '__ac': 'SESSIONDATA'}}

        expected = {
            'session': {
                '__ac': REPLACEMENT}}

        self.assertEquals(expected, cleanup_request_info(input))

    def test_ac_cookie_is_removed_from_cookie(self):
        input = {
            'cgi-data': {
                'HTTP_COOKIE': '__ac="SESSION"'}}

        expected = {
            'cgi-data': {
                'HTTP_COOKIE': '__ac="%s"' % (
                    REPLACEMENT)}}

        self.assertEquals(expected, cleanup_request_info(input))

    def test_ac_cookie_is_removed_from_man_cookies(self):
        input = {
            'cgi-data': {
                'HTTP_COOKIE': 'foo=Foo; __ac="COOKIEDATA"; bar=Bar; baz=Baz'}}

        expected = {
            'cgi-data': {
                'HTTP_COOKIE': 'foo=Foo; __ac="%s"; bar=Bar; baz=Baz' % (
                    REPLACEMENT)}}

        self.assertEquals(expected, cleanup_request_info(input))

    def test_ac_cookie_is_removed_from_cgi_data(self):
        input = {
            'cgi-data': {
                'OTHER___AC': 'COOKIEDATA'}}

        expected = {
            'cgi-data': {
                'OTHER___AC': REPLACEMENT}}

        self.assertEquals(expected, cleanup_request_info(input))
