from errbit.client import Client
from zope.component.hooks import getSite
import logging
import sys


class ErrbitLoggingHandler(logging.Handler):

    def emit(self, record):
        exc_info = sys.exc_info()
        if exc_info[0] is None:
            return

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
        cgidata['other'] = request.other

        return {
            'url': request.getURL(),
            'params': request.form,
            'session': request.cookies,
            'cgi-data': dict(request.environ)}
