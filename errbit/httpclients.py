import requests
import urllib
import urllib2


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


class Urllib2HTTPClient(object):

    def post(self, url, encoded_post_data):
        request = urllib2.Request(url=url, data=encoded_post_data)
        urllib2.urlopen(request)


HTTP_CLIENTS['urllib2'] = Urllib2HTTPClient
