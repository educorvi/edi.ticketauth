# -*- coding: utf-8 -*-
from edi.ticketauth.content.ticket import ITicket  # NOQA E501
from edi.ticketauth.testing import EDI_TICKETAUTH_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class TicketIntegrationTest(unittest.TestCase):

    layer = EDI_TICKETAUTH_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_ticket_schema(self):
        fti = queryUtility(IDexterityFTI, name='Ticket')
        schema = fti.lookupSchema()
        self.assertEqual(ITicket, schema)

    def test_ct_ticket_fti(self):
        fti = queryUtility(IDexterityFTI, name='Ticket')
        self.assertTrue(fti)

    def test_ct_ticket_factory(self):
        fti = queryUtility(IDexterityFTI, name='Ticket')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ITicket.providedBy(obj),
            u'ITicket not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_ticket_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Ticket',
            id='ticket',
        )

        self.assertTrue(
            ITicket.providedBy(obj),
            u'ITicket not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('ticket', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('ticket', parent.objectIds())

    def test_ct_ticket_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Ticket')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
