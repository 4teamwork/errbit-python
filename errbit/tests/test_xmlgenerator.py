from errbit.xmlgenerator import generate_xml
from lxml import etree
from pyquery import PyQuery
from unittest2 import TestCase
import os
import sys


def node_to_json(node):
    data = dict(node.items())
    data['_tag'] = node.tag
    if node.text:
        data['_text'] = node.text
    return data


def line_node_to_json(node):
    data = node_to_json(node)
    if data['file']:
        path_parts = data['file'].split('/')
        errbit_pos = path_parts.index('errbit')
        data['file'] = '/'.join(['...'] + path_parts[errbit_pos:])
    if data['number']:
        data['number'] = '...line number...'
    return data


def vars_to_json(nodes):
    data = {}
    for node in nodes:
        node_data = node_to_json(node)

        if node.getchildren():
            value = vars_to_json(node.getchildren())
        else:
            value = node_data.get('_text')

        data[node_data.get('key')] = value
    return data


def validate_xml(xml):
    dtd_path = os.path.join(os.path.dirname(__file__), 'assets', 'airbrake_2_3.xsd')
    schema_root = etree.XML(open(dtd_path, 'r').read())
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema=schema)
    return etree.fromstring(xml, parser)


def generate(*args, **kwargs):
    xml = generate_xml(*args, **kwargs)
    validate_xml(xml)
    return PyQuery(xml)


try:
    raise AttributeError("Foo instance has no attribute 'bar'")
except:
    EXC_INFO = sys.exc_info()

try:
    raise Exception('')
except:
    EMPTY_EXC_INFO = sys.exc_info()


NOTIFIER = {'name': 'my project',
            'url': 'http://localhost/',
            'version': '1.3'}


class TestXMLGenerator(TestCase):

    def test_api_key_is_in_xml(self):
        api_key = 'abcd1234'
        doc = generate(api_key, NOTIFIER, EXC_INFO)
        self.assertEquals(api_key, doc('api-key').text())

    def test_noitifier_info_in_xml(self):
        doc = generate('', NOTIFIER, EXC_INFO)
        self.assertEquals('my project', doc('notifier name').text())

    def test_exception_class_in_xml(self):
        doc = generate('', NOTIFIER, EXC_INFO)
        self.assertEquals('AttributeError', doc('error class').text())

    def test_exception_message_in_xml(self):
        msg = "Foo instance has no attribute 'bar'"
        doc = generate('', NOTIFIER, EXC_INFO)
        self.assertEquals(msg, doc('error message').text())

    def test_message_shall_not_be_empty(self):
        doc = generate('', NOTIFIER, EMPTY_EXC_INFO)
        self.assertIn('<message> </message>', str(doc))

    def test_backtrace_in_xml(self):
        try:
            raise AttributeError("Peter")
        except:
            exc_info = sys.exc_info()

        doc = generate('', NOTIFIER, exc_info)
        self.assertEquals([{'_tag': 'line',
                            'method': 'test_backtrace_in_xml',
                            'file': '.../errbit/tests/test_xmlgenerator.py',
                            'number': '...line number...'}],

                          map(line_node_to_json,
                              doc('error backtrace line')))

    def test_request_url(self):
        request = {'url': 'http://localhost/foo/bar'}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals('http://localhost/foo/bar', doc('request url').text())

    def test_request_component(self):
        request = {'component': 'folders'}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals('folders', doc('request component').text())

    def test_request_action(self):
        request = {'action': 'list'}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals('list', doc('request action').text())

    def test_request_params(self):
        request = {'params': {'foo': 'bar'}}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals({'foo': 'bar'}, vars_to_json(doc('request params var')))

    def test_request_params_with_ints(self):
        request = {'params': {'foo': 5}}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals({'foo': '5'}, vars_to_json(doc('request params var')))

    def test_request_params_nested(self):
        request = {'params': {'foo': {'bar': 'BAR', 'baz': 'BAZ'}}}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals({'foo': {'bar': 'BAR', 'baz': 'BAZ'}},
                          vars_to_json(doc('request params > var')))

    def test_request_session(self):
        request = {'session': {'foo': 'bar'}}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals({'foo': 'bar'}, vars_to_json(doc('request session var')))

    def test_request_cgi_data(self):
        request = {'cgi-data': {'foo': 'bar'}}
        doc = generate('', NOTIFIER, EXC_INFO, request=request)
        self.assertEquals({'foo': 'bar'}, vars_to_json(doc('request cgi-data var')))

    def test_environment_name_in_xml(self):
        environment = {'environment-name': 'staging'}
        doc = generate('', NOTIFIER, EXC_INFO, environment=environment)
        self.assertEquals('staging', doc('server-environment environment-name').text())

    def test_environment_app_version(self):
        environment = {'app-version': '1.5'}
        doc = generate('', NOTIFIER, EXC_INFO, environment=environment)
        self.assertEquals('1.5', doc('server-environment app-version').text())
