from errbit.client import Client
from zope.component.hooks import getSite
import logging
import re
import sys


REPLACEMENT = '**removed by errbit-python**'
FORMDATA_FILTERS = [r'.*pass.*']
SESSIONDATA_FILTERS = [r'^__ac']


def match_any(expressions, text):
    for expr in expressions:
        if re.match(expr, text):
            return True
    return False


def filter_values(data, key_expressions):
    if not data:
        return data

    new_data = {}
    for key, value in data.items():
        if match_any(key_expressions, key):
            new_data[key] = REPLACEMENT
        else:
            new_data[key] = value

    return new_data


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

        component = self.get_component(request)
        action = self.get_action(request)

        return {
            'url': request.getURL(),
            'params': filter_values(request.form, FORMDATA_FILTERS),
            'session': filter_values(request.cookies, SESSIONDATA_FILTERS),
            'cgi-data': cgidata,
            'component': component,
            'action': action}

    def get_component(self, request):
        # We use the portal_type of the current context as component,
        # with a fallback to its class name.
        if not getattr(request, 'PARENTS', None):
            return ''

        obj = request.PARENTS[0]
        return getattr(obj, 'portal_type', obj.__class__.__name__)

    def get_action(self, request):
        # We use the name of the view as action.
        view = getattr(request, 'PUBLISHED', None)
        if not view:
            return

        return getattr(view, '__name__', view.__class__.__name__)
