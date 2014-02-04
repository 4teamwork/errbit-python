from StringIO import StringIO
from errbit.request import ThreadedRequest
from errbit.tests.utils import NothingRaised
from unittest2 import TestCase


class MockHTTPClient(object):

    def __init__(self):
        self.posted = []

    def post(self, url, encoded_post_data):
        self.posted.append({'url': url,
                            'data': encoded_post_data})


class ErrorMockHTTPClient(object):

    def post(self, url, encoded_post_data):
        raise Exception('HTTP Error')


class TestThreadedRequest(TestCase):

    def test_request_is_sent(self):
        http_client = MockHTTPClient()

        req = ThreadedRequest('http://foo/bar', '<data></data>',
                              http_client=http_client)
        req.start()
        req.join()

        self.assertEquals([{'url': 'http://foo/bar',
                            'data': '<data></data>'}],
                          http_client.posted)

    def test_exceptions_are_catched_and_printed(self):
        http_client = ErrorMockHTTPClient()
        log = StringIO()
        req = ThreadedRequest('http://foo/bar',
                              '<data></data>',
                              http_client=http_client,
                              log=log)

        with NothingRaised():
            req.start()
            req.join()

        self.assertEquals('ERROR: Failed to post to errbit: Exception: HTTP Error',
                          log.getvalue())
