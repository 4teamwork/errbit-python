import requests


HTTP_CLIENTS = {}


class RequestsHTTPClient(object):

    def post(self, url, encoded_post_data):
        response = requests.post(url, data=encoded_post_data)
        response.raise_for_status()


HTTP_CLIENTS['requests'] = RequestsHTTPClient
