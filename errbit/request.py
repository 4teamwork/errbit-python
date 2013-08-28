import logging
import requests
import threading


class ThreadedRequest(threading.Thread):

    def __init__(self, url, data):
        super(ThreadedRequest, self).__init__()
        self.url = url
        self.data = data

    def run(self):
        try:
            self.post_request()
        except Exception, e:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.ERROR)
            logger.exception(e)

    def post_request(self):
        response = requests.post(self.url, data=self.data)
        response.raise_for_status()
