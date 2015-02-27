from errbit.utils import logging_exceptions
from StringIO import StringIO
from unittest2 import TestCase
import logging



class TestLoggingErrors(TestCase):

    def setUp(self):
        self.logstream = StringIO()
        self.handler = logging.StreamHandler(self.logstream)
        logging.root.addHandler(self.handler)
        self.original_log_level = logging.root.level
        logging.root.setLevel(logging.ERROR)

    def tearDown(self):
        logging.root.removeHandler(self.handler)
        logging.root.level = self.original_log_level

    def get_log(self):
        self.handler.flush()
        return self.logstream.getvalue()

    def test_logs_exceptions(self):
        @logging_exceptions
        def foo():
            raise KeyError('bar')

        with self.assertRaises(KeyError) as cm:
            foo()
        self.assertTrue(cm.exception._errbit_do_not_report)

        log_lines = self.get_log().strip().splitlines()
        self.assertEquals('exception while trying to report other exception:',
                          log_lines[0])
        self.assertEquals('KeyError: \'bar\'',
                          log_lines[-1])
