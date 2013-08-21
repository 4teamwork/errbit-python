from errbit.client import Client
from zope.component.hooks import getSite
import logging
import sys


class ErrbitLoggingHandler(logging.Handler):

    def __init__(self):
        super(ErrbitLoggingHandler, self).__init__()
        self.setLevel(logging.ERROR)
        self._last_exception = None

    def emit(self, record):
        exc_info = sys.exc_info()
        if exc_info[0] is None:
            return

        # This is a logging handler, not an exception handler.
        # By storing the last consumed exception we can make the handler
        # only report on new exceptions.
        if self._last_exception == exc_info:
            return
        else:
            self._last_exception = exc_info

        try:
            self.notify_errbit(exc_info)
        except:
            pass

    def notify_errbit(self, exc_info):
        client = Client()
        client.post(exc_info, request=self.get_request_info())

    def get_request_info(self):
        request = getattr(getSite(), 'REQUEST', None)
        if not request:
            return None

        cgidata = dict(request.environ)
        for key, value in request.other.items():
            cgidata['other.%s' % key] = value

        return {
            'url': request.getURL(),
            'params': request.form,
            'session': request.cookies,
            'cgi-data': cgidata}
