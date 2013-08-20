from errbit import xmlgenerator
from errbit.request import ThreadedRequest
import logging
import os
import pkg_resources


LOG = logging.getLogger('errbit')


def get_version(package):
    return pkg_resources.require(package)[0].version


class Client(object):

    def post(self, exc_info, request=None, environment=None):
        if not self.get_errbit_url():
            logging.error('ERRBIT_URL not configured as environment variable.')

        if not self.get_api_key():
            logging.error('ERRBIT_API_KEY not configured as environment variable.')

        xml = xmlgenerator.generate_xml(self.get_api_key(), self.get_notifier(),
                                        exc_info, request=request,
                                        environment=environment)

        req = ThreadedRequest(self.get_errbit_url(), xml)
        req.start()

    def get_api_key(self):
        return os.environ.get('ERRBIT_API_KEY')

    def get_errbit_url(self):
        return os.environ.get('ERRBIT_URL')

    def get_notifier(self):
        package = os.environ.get('ERRBIT_NOTIFIER_PACKAGE', 'errbit')

        data = {'name': os.environ.get('ERRBIT_NOTIFIER_NAME', package),
                'version': os.environ.get('ERRBIT_NOTIFIER_VERSION',
                                          get_version(package)),
                'url': os.environ.get('ERRBIT_NOTIFIER_URL', '')}

        return data
