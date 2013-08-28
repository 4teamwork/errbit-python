import sys


try:
    import errbit
except ImportError:
    print 'You should start this script with: ' + \
        './bin/zopepy scripts/test-posting-to-4teamwork.py'
    sys.exit(1)


import os
import socket


os.environ['ERRBIT_URL'] = 'https://errbit.4teamwork.ch/notifier_api/v2/notices'
print 'This will post to', os.environ['ERRBIT_URL']
os.environ['ERRBIT_PACKAGE'] = 'errbit'
os.environ['ERRBIT_ENVIRONMENT'] = socket.gethostname()
os.environ['ERRBIT_API_KEY'] = raw_input('Errbit API-Key: ').strip()
print ''

from errbit.httpclients import HTTP_CLIENTS
http_client = '-'
print 'Please Select the HTTP client implementation. Valid implementations:'
print ' -', '\n - '.join(HTTP_CLIENTS.keys())

while http_client and http_client not in HTTP_CLIENTS.keys():
    http_client = raw_input('Client (Default: "requests"): ').strip()

os.environ['ERRBIT_HTTP_CLIENT'] = http_client or 'requests'
print ''


class ErrbitPythonClientTesting(Exception):
    pass


from errbit.client import Client

client = Client()
try:
    raise ErrbitPythonClientTesting('We have an exception!')
except:
    exc_info = sys.exc_info()

    request = {
        'url': 'http://my.app/app/folders/create',
        'component': 'folders',
        'action': 'create',
        'params': {
            'title': 'My Folder'},
        'session': {
            'cookie': 'session_id=123345'},
        'cgi-data': {
            'ERRBIT_HTTP_CLIENT': os.environ['ERRBIT_HTTP_CLIENT']}}

    client.post(exc_info, request=request)

print ''
