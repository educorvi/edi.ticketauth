# -*- coding: utf-8 -*-

from edi.ticketauth import _
from Products.Five.browser import BrowserView
from plone import api as ploneapi
import requests

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Newticket(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('newticket.pt')

    def __call__(self):
        self.login = {'login': 'admin', 'password': 'admin'}
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
        payload = {'email': email}
        headers = {'Accept': 'application/json','Authorization': 'Bearer %s' % authtoken}
        result = requests.get(url, params=payload, headers=headers, verify=False)
        resultdata = result.json()
        if resultdata['status'] == 'success':
            #ploneapi.statusmeldung('Ihnen wurde eine E-Mail mit dem Ticket zugestellt')
            ploneapi.portal.show_message(message='Ihnen wurde eine E-Mail mit dem Ticket zugestellt', request=self.request, type='info')
        else:
            ploneapi.portal.show_message(message='Es ist uns ein Fehler unterlaufen', request=self.request, type='error')
        return

