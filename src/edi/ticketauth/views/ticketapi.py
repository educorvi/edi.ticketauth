# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
import jsonlib
from plone import api as ploneapi
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import logging
from edi.ticketauth.content.ticket import titlefactory, ticketfactory, validfactory

logger = logging.getLogger("edi.ticketauth")

class Ticketapi(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        email = self.request.get('email')
        local = self.request.get('local')
        if not email:
            result = {'status': 'error', 'message': 'Fehler bei der Übermittlung der E-Mail-Adresse'}
            return jsonlib.write(result)
        result = self.get_new_ticket(email)
        if result.get('status') == 'success' and local == 'local':
            self.send_mail_with_ticket(email, result.get('ticket'))
        return jsonlib.write(result)

    def send_mail_with_ticket(self, email, ticket):
        member = ploneapi.user.get(username=email)
        name = member.getProperty('fullname')
        portalname = ploneapi.portal.get().title
        portalurl = ploneapi.portal.get().absolute_url() + '/login'
        ticketgueltigkeit = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.validtime')
        mailsubject = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.mailsubject')
        mailtext = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.mailtext')
        mailtext = Template(mailtext).render(name=name, portalname=portalname, ticketgueltigkeit=ticketgueltigkeit, 
                email=email, ticket=ticket, portalurl=portalurl)
        mime_msg = MIMEMultipart('related')
        mime_msg['Subject'] = mailsubject
        mime_msg['From'] = ploneapi.portal.get_registry_record('plone.email_from_address')
        mime_msg['To'] = email
        mime_msg.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        mime_msg.attach(msgAlternative)
        msg_text = MIMEText(mailtext, _subtype='html', _charset='utf-8')
        msgAlternative.attach(msg_text)
        mail_host = ploneapi.portal.get_tool(name='MailHost')
        mail_host.send(mime_msg.as_string())
        logmessage = 'E-Mail gesendet an: %s' % email
        logger.info(logmessage)

    def get_new_ticket(self, email):
        user = ploneapi.user.get(username=email) 
        if not user:
            result = {'status': 'error', 'message': 'Für diese E-Mail Adresse kann leider kein Ticket ausgestellt werden.'}
            return result
        userid = user.getId()
        membership = ploneapi.portal.get_tool(name='portal_membership')
        memberfolder = membership.getHomeFolder(userid)
        if not memberfolder:
            result = {'status': 'error', 'message': 'Für diese E-Mail Adresse kann leider kein Ticket ausgestellt werden.'}
            return result
        ticketobject = ploneapi.content.create(type='Ticket',
                                               title=titlefactory(),
                                               valid=validfactory(),
                                               ticket=ticketfactory(),
                                               container=memberfolder)
        ticket = ticketobject.ticket
        result = {'status':'success', 'ticket':ticket}
        return result
