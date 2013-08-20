import logging
import requests
import threading


def log_error(method):
    def wrap_error(*args, **kwargs):
        try:
            if len(kwargs):
                method(**kwargs)
            else:
                method(*args)
        except Exception, e:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.ERROR)
            logger.exception(e)

    wrap_error.__name__ = method.__name__
    return wrap_error


class ThreadedRequest(threading.Thread):

    def __init__(self, url, data):
        super(ThreadedRequest, self).__init__()
        self.url = url
        self.data = data

    @log_error
    def run(self):
        response = requests.post(self.url, data=self.data)
        response.raise_for_status()
