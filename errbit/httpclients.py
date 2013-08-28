import requests
import urllib


HTTP_CLIENTS = {}


class RequestsHTTPClient(object):

    def post(self, url, encoded_post_data):
        response = requests.post(url, data=encoded_post_data)
        response.raise_for_status()


HTTP_CLIENTS['requests'] = RequestsHTTPClient


class UrllibHTTPClient(object):

    def post(self, url, encoded_post_data):
        response = urllib.urlopen(url, encoded_post_data)
        body = response.read()
        if not str(response.code).startswith('2'):
            raise Exception('%s: %s' % (response.code, body))


HTTP_CLIENTS['urllib'] = UrllibHTTPClient
