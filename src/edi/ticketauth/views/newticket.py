# -*- coding: utf-8 -*-

from edi.ticketauth import _
from Products.Five.browser import BrowserView

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Newticket(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('newticket.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')

        email = self.request.get('email')
        if email:
            self.create_ticket(email)

        return self.index()

    def create_ticket(self):
        authtoken = self.AuthToken()
