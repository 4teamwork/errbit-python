import logging
import re

LOG = logging.getLogger('errbit.plone.cleanups')


CLEANUPS = []
REPLACEMENT = '**removed by errbit-python**'


def cleanup(func):
    """Decorator for registering cleanup functions.
    """
    CLEANUPS.append(func)
    return func


def cleanup_request_info(request):
    """Applies all cleanups to the request info data.
    """

    for cleanup in CLEANUPS:
        try:
            request = cleanup(request)
        except Exception, exc:
            logging.DEBUG('Failed to apply cleanup (%s): %s' % (
                    str(cleanup), str(exc)))

    return request


def filter_values(data, key_expression):
    if not data:
        return data

    new_data = {}
    xpr = re.compile(key_expression, re.IGNORECASE)
    for key, value in data.items():
        if xpr.match(key):
            new_data[key] = REPLACEMENT
        else:
            new_data[key] = value

    return new_data

@cleanup
def filter_password_from_params(request):
    if 'params' in request:
        request['params'] = filter_values(request['params'], r'.*pass')
    return request


@cleanup
def filter_ac_cookie(request):
    if 'session' in request:
        request['session'] = filter_values(request['session'], r'^__ac')

    if 'cgi-data' in request and 'HTTP_COOKIE' in request['cgi-data']:
        request['cgi-data']['HTTP_COOKIE'] = re.sub(
            r'(__ac)=[^;]*(;?)',
            r'\g<1>="%s"\g<2>' % REPLACEMENT,
            request['cgi-data']['HTTP_COOKIE'])

    if 'cgi-data' in request:
        request['cgi-data'] = filter_values(request['cgi-data'], r'.*__ac')


    return request
