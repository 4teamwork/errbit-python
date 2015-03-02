from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class ErrbitPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="errbit" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'errbit.ploneintegration:default')


ERRBIT_PLONE_FIXTURE = ErrbitPloneLayer()
ERRBIT_PLONE_FUNCTIONAL = FunctionalTesting(
    bases=(ERRBIT_PLONE_FIXTURE, ),
    name='errbit.plone:integration')
