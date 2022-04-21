# -*- coding: utf-8 -*-

from edi.ticketauth import _
from Products.Five.browser import BrowserView
from plone import api as ploneapi
import requests

class Newticket(BrowserView):

    def __call__(self):
        ticketlogin = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.ticketlogin')
        ticketpassword = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.ticketpassword')
        self.login = {'login': ticketlogin, 'password': ticketpassword}
        self.formtitle = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.formtitle')
        self.formhelp = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.formhelp')
        self.tickettitle = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.tickettitle')
        self.authurl = ploneapi.portal.get().absolute_url()+'/@login' 
        email = self.request.get('email')
        if email:
            self.create_ticket(email)
        return self.index()

    def getAuthToken(self):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        token = requests.post(self.authurl, headers=headers, json=self.login)
        return token.json().get('token')

    def create_ticket(self, email):
        authtoken = self.getAuthToken()
        url = ploneapi.portal.get().absolute_url()+'/ticketapi' 
        payload = {'email': email, 'local': 'local'}
        headers = {'Accept': 'application/json','Authorization': 'Bearer %s' % authtoken}
        result = requests.get(url, params=payload, headers=headers, verify=False)
        resultdata = result.json()
        if resultdata['status'] == 'success':
            statusmessage = f"Ihnen wurde gerade eine E-Mail mit dem neuen {self.tickettitle} zugestellt. Bitte schauen Sie auch in Ihren SPAM-Ordner."
            ploneapi.portal.show_message(message=statusmessage, request=self.request, type='info')
        else:
            ploneapi.portal.show_message(message=resultdata['message'], request=self.request, type='error')
        return
