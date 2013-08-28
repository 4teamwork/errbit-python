import sys
import threading


class ThreadedRequest(threading.Thread):

    def __init__(self, url, data, http_client, log=None):
        super(ThreadedRequest, self).__init__()
        self.url = url
        self.data = data
        self.http_client = http_client
        self.log = log or sys.stdout

    def run(self):
        try:
            self.http_client.post(self.url, self.data)
        except Exception, exc:
            self.log.write('ERROR: Failed to post to errbit: %s: %s' % (
                    exc.__class__.__name__, str(exc)))
