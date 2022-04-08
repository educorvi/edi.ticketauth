# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.ticketauth


class EdiTicketauthLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.ticketauth)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.ticketauth:default')


EDI_TICKETAUTH_FIXTURE = EdiTicketauthLayer()


EDI_TICKETAUTH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_TICKETAUTH_FIXTURE,),
    name='EdiTicketauthLayer:IntegrationTesting',
)


EDI_TICKETAUTH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_TICKETAUTH_FIXTURE,),
    name='EdiTicketauthLayer:FunctionalTesting',
)


EDI_TICKETAUTH_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_TICKETAUTH_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiTicketauthLayer:AcceptanceTesting',
)
