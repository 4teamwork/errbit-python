from Products.Five.browser import BrowserView
import os


class ErrbitTestingException(Exception):
    """An exception for testing the errbit connection.
    """


class MakeError(BrowserView):

    def __call__(self):
        raise ErrbitTestingException('Testing the errbit connection.')


class ErrbitJavaScript(BrowserView):

    def __call__(self):
        self.request.response.setHeader(
            'Content-Type', 'application/javascript; charset=utf-8')
        if not self.available():
            return ''

        return '\n'.join((self.get_airbrake_shim_js(),
                          '',
                          self.get_configuration_js()))

    def available(self):
        required = set(('ERRBIT_URL', 'ERRBIT_APP_ID',
                        'ERRBIT_API_KEY', 'ERRBIT_ENVIRONMENT'))
        return not bool(required - set(os.environ.keys()))

    def get_airbrake_shim_js(self):
        path = os.path.join(os.path.dirname(__file__),
                            'resources',
                            'airbrake-shim.js')
        with open(path) as shim:
            return shim.read()

    def get_configuration_js(self):
        url = os.environ['ERRBIT_URL'].split('/notifier_api', 1)[0]
        return '\n'.join(
            ('Airbrake.onload = function(client) {{'
             '  client.setProject("{ERRBIT_APP_ID}", "{ERRBIT_API_KEY}");',
             '  client.setHost("{0}");'.format(url),
             '  client.setEnvironmentName("{ERRBIT_ENVIRONMENT}");',
             '}};')).format(**os.environ)
