# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
import jsonlib
from plone import api as ploneapi
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class Ticketapi(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        email = self.request.get('email')
        if not email:
            result = {'status': 'error', 'message': 'Fehler bei der Übermittlung der E-Mail-Adresse'}
            return jsonlib.write(result)
        self.get_new_ticket(email)

    def get_new_ticket(self, email):
        user = ploneapi.user.get(username=email) 
        if not user:
            result = {'status': 'error', 'message': 'Für diese E-Mail Adresse kann leider kein Ticket ausgestellt werden.'}
            return jsonlib.write(result)
        userid = user.getId()
        membership = ploneapi.portal.get_tool(name='portal_membership')
        memberfolder = membership.getHomeFolder(userid)
        if not memberfolder:
            result = {'status': 'error', 'message': 'Für diese E-Mail Adresse kann leider kein Ticket ausgestellt werden.'}
            return jsonlib.write(result)
 
        ticketobject = ploneapi.content.create(type='Ticket', title='Ticket', container=memberfolder)
        ticket = ticketobject.ticket
        print(ticket)
        #ploneapi.sendEmailWithTicket
        result = {'status':'success', 'message':''}
        return jsonlib.write(result) 
