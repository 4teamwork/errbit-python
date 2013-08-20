from StringIO import StringIO
from errbit.request import ThreadedRequest
from mocker import ARGS
from mocker import KWARGS
from mocker import MockerTestCase
from requests.exceptions import HTTPError
import logging


class TestThreadedRequest(MockerTestCase):

    def setUp(self):
        self.requests = self.mocker.replace('requests')
        self.expect(self.requests.post(ARGS, KWARGS)).count(0)

        self.log = StringIO()
        self.handler = logging.StreamHandler(self.log)
        logging.root.addHandler(self.handler)

    def tearDown(self):
        logging.root.removeHandler(self.handler)

    def test_request_is_sent(self):
        self.expect_request('http://foo/bar', '<data></data>')
        self.mocker.replay()

        req = ThreadedRequest('http://foo/bar', '<data></data>')
        req.run()  # synced call

    def test_exceptions_are_catched_and_logged(self):
        self.expect_request('http://foo', 'data', throws=500)
        self.mocker.replay()

        ThreadedRequest('http://foo', 'data').run()
        self.assertIn('http error 500', self.read_log())

    def expect_request(self, url, data, throws=None):
        response = self.mocker.mock()
        self.expect(self.requests.post(url, data=data)).result(response)
        self.expect(response.raise_for_status())
        if throws:
            self.mocker.throw(HTTPError('http error %s' % throws))

    def read_log(self):
        self.log.seek(0)
        return self.log.read().strip().split('\n')
