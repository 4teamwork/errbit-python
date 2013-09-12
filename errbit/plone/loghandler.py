from errbit.client import Client
from errbit.plone.cleanup import cleanup_request_info
from zope.component.hooks import getSite
import logging
import sys


class ErrbitLoggingHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
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
        request_info = self.get_request_info()
        request_info = cleanup_request_info(request_info)
        client.post(exc_info, request=request_info)

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
            'params': request.form,
            'session': request.cookies,
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
