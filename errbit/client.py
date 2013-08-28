from errbit import httpclients
from errbit import xmlgenerator
from errbit.request import ThreadedRequest
import logging
import os
import pkg_resources


LOG = logging.getLogger('errbit')


def get_version(package):
    return pkg_resources.require(package)[0].version


class Client(object):

    def post(self, exc_info, request=None):
        if not self.get_errbit_url():
            logging.error('ERRBIT_URL not configured as environment variable.')

        if not self.get_api_key():
            logging.error('ERRBIT_API_KEY not configured as environment variable.')

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

    def get_environment(self):
        data = {'project-root': os.getcwd()}

        env_name = os.environ.get('ERRBIT_ENVIRONMENT', None)
        if env_name:
            data['environment-name'] = env_name

        package = os.environ.get('ERRBIT_PACKAGE', None)
        if package:
            data['app-version'] = get_version(package)

        return data
