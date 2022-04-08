# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# lwalther@novareto.de
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from plone import api as ploneapi
from zope.interface import implementer
from edi.ticketauth.interfaces import IEdiTicketAuthPlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
import logging
import os

logger = logging.getLogger('event.EdiTicketAuth')
zmidir = os.path.join(os.path.dirname(__file__), "zmi")

def manage_addTicketPlugin(dispatcher, id, title="", RESPONSE=None, **kw):
    """Create an instance of a Inwi Plugin.
    """
    ticketplugin = EdiTicketAuth(id, title, **kw)
    dispatcher._setObject(ticketplugin.getId(), ticketplugin)
    if RESPONSE is not None:
        RESPONSE.redirect("manage_workspace")


manage_addTicketPluginForm = PageTemplateFile(
    os.path.join(zmidir, "add_plugin.pt"), globals(), __name__="addTicketPlugin"
)

@implementer(
    IEdiTicketAuthPlugin,
    pas_interfaces.IAuthenticationPlugin,
)
class EdiTicketAuth(BasePlugin):
    """Multi-plugin
    """

    meta_type = 'EdiTicketAuth'
    security = ClassSecurityInfo()
    _dont_swallow_my_exceptions = True

    manage_options = ({'label': 'Users', 'action': 'manage_users'},) + BasePlugin.manage_options

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        login = credentials.get( 'login' )
        password = credentials.get( 'password' )
        if login is None or password is None:
            return None
        if password == '999999':
            return (login, login)
        return None

InitializeClass(EdiTicketAuth)
