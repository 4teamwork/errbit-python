import traceback
import xmlbuilder


SCHEMA_VERSION = '2.3'


def generate_xml(api_key, notifier, exc_info, request=None, environment=None):
    request = request or {}

    xml = xmlbuilder.XMLBuilder('notice', version=SCHEMA_VERSION)
    getattr(xml, 'api-key')(api_key)

    with xml.notifier:
        xml.name(notifier.get('name', ''))
        xml.version(notifier.get('version'))
        xml.url(notifier.get('url'))

    if exc_info:
        with xml.error:
            add_xml_error(xml, exc_info)

    if request:
        with xml.request:
            add_xml_request(xml, request)

    with getattr(xml, 'server-environment'):
        add_xml_server_environment(xml, environment or {})

    return str(xml)


def add_xml_error(xml, exc_info):
    exc_type, exc_value, exc_traceback = exc_info

    getattr(xml, 'class')(exc_type.__name__)
    message = str(exc_value)
    if message:
        xml.message(message)
    else:
        xml.message(' ')

    with xml.backtrace:
        for path, lineno, method, line in traceback.extract_tb(exc_traceback):
            xml.line(method=method, file=path, number=str(lineno))


def add_xml_request(xml, request):
    xml.url(request.get('url', ''))
    xml.component(request.get('component', ''))
    xml.action(request.get('action', ''))

    if request.get('params', None):
        with xml.params:
            add_xml_dict_vars(xml, request.get('params'))

    if request.get('session', None):
        with xml.session:
            add_xml_dict_vars(xml, request.get('session'))

    if request.get('cgi-data', None):
        with getattr(xml, 'cgi-data'):
            add_xml_dict_vars(xml, request.get('cgi-data'))


def add_xml_server_environment(xml, environment):
    getattr(xml, 'environment-name')(environment.get('environment-name', 'unkown'))
    if environment.get('app-version', None):
        getattr(xml, 'app-version')(environment.get('app-version'))

    if environment.get('project-root', None):
        getattr(xml, 'project-root')(environment.get('project-root'))


def add_xml_dict_vars(xml, data):
    for key, value in data.items():
        if isinstance(value, dict):
            with xml.var(key=key):
                add_xml_dict_vars(xml, value)

        else:
            xml.var(str(value), key=key)
