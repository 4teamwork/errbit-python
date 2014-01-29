from errbit import httpclients
from errbit import xmlgenerator
from errbit.request import ThreadedRequest
import json
import logging
import os
import pkg_resources
import re
import sys
import traceback


LOG = logging.getLogger('errbit')


def get_version(package):
    return pkg_resources.require(package)[0].version


class ErrbitInvalidConfigFileException(Exception):
    pass


class Client(object):

    def post(self, exc_info, request=None):
        if not self.get_errbit_url():
            logging.error('ERRBIT_URL not configured as environment variable.')

        if not self.get_api_key():
            logging.error('ERRBIT_API_KEY not configured as environment variable.')

        if self.is_ignored(exc_info):
            return

        xml = xmlgenerator.generate_xml(self.get_api_key(),
                                        self.get_notifier(),
                                        exc_info, request=request,
                                        environment=self.get_environment())

        http_client = self.http_client()
        req = ThreadedRequest(self.get_errbit_url(), xml, http_client=http_client)
        req.start()

    def http_client(self):
        client_name = os.environ.get('ERRBIT_HTTP_CLIENT', 'requests')
        if client_name not in httpclients.HTTP_CLIENTS:
            raise Exception(('ERRBIT_HTTP_CLIENT: "%s" is no valid client name. '
                             'Valid clients are: %s') % (
                    client_name, str(httpclients.HTTP_CLIENTS.keys())))

        return httpclients.HTTP_CLIENTS.get(client_name)()

    def get_api_key(self):
        return os.environ.get('ERRBIT_API_KEY')

    def get_errbit_url(self):
        return os.environ.get('ERRBIT_URL')

    def get_notifier(self):
        return {'name': 'errbit',
                'version': get_version('errbit'),
                'url': 'https://github.com/4teamwork/errbit-python'}

    def get_ignore_regex(self):
        cfg_path = os.environ.get('ERRBIT_IGNORE')
        if not cfg_path:
            return []

        try:
            cfg = json.load(open(cfg_path, 'r'))
            return cfg['exception_msg']
        except Exception, exc:
            raise ErrbitInvalidConfigFileException(': '.join((exc.__class__.__name__, str(exc))))

    def is_ignored(self, exc_info):
        exc_message = traceback.format_exception_only(exc_info[0], exc_info[1])[-1].strip('\n')

        if exc_info[0] != ErrbitInvalidConfigFileException:
            try:
                ignore_pattern = [re.compile(pat) for pat in self.get_ignore_regex()]
                for pat in ignore_pattern:
                    if pat.match(exc_message):
                        return True
            except ErrbitInvalidConfigFileException:
                self.post(sys.exc_info())
        return False

    def get_environment(self):
        data = {'project-root': os.getcwd()}

        env_name = os.environ.get('ERRBIT_ENVIRONMENT', None)
        if env_name:
            data['environment-name'] = env_name

        package = os.environ.get('ERRBIT_PACKAGE', None)
        if package:
            data['app-version'] = get_version(package)

        return data
