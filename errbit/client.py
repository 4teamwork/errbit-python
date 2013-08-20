import os
import pkg_resources


def get_version(package):
    return pkg_resources.require(package)[0].version


class Client(object):

    def get_api_key(self):
        return os.environ.get('ERRBIT_API_KEY')

    def get_notifier(self):
        package = os.environ.get('ERRBIT_NOTIFIER_PACKAGE', 'errbit')

        data = {'name': os.environ.get('ERRBIT_NOTIFIER_NAME', package),
                'version': os.environ.get('ERRBIT_NOTIFIER_VERSION',
                                          get_version(package))}

        if os.environ.get('ERRBIT_NOTIFIER_URL'):
            data['url'] = os.environ.get('ERRBIT_NOTIFIER_URL')

        return data
