# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# lwalther@novareto.de
from datetime import datetime
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
from plone import api

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
    pas_interfaces.IUserEnumerationPlugin,
    pas_interfaces.IPropertiesPlugin,
    pas_interfaces.IGroupsPlugin
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
        ticketmethod = ploneapi.portal.get_registry_record(name='ticketmethod', default=1)
        if ticketmethod == 1:
            member = ploneapi.user.get(username = login)
            if not member:
                return None
            userid = member.getId()
            membership = ploneapi.portal.get_tool(name='portal_membership')
            homefolder = membership.getHomeFolder(userid)
            if not homefolder:
                return None
            tickets = homefolder.contentItems()
            for i in tickets:
                ticket = i[1]
                if ticket.portal_type == "Ticket":
                    if ticket.valid > datetime.now():
                        if ticket.ticket == password:
                            return (userid, login)
        elif ticketmethod == 2:
            user = ploneapi.content.find(portal_type='Benutzer', mandant_userid=login)
            if not user:
                return None
            logged = user[0].getObject()
            if logged.password == password:
                return (login, login)
        return None

    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=False, sort_by=None, max_results=None, **kw):

        ticketmethod = ploneapi.portal.get_registry_record(name='ticketmethod', default=1)
        if ticketmethod == 1:
            return list()

        key = login or id
        mylist = []
        if key:
            users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=key)
            for i in users:
                mylist.append({
                               "id" : i.mandant_userid,
                               "login" : i.mandant_userid,
                               "pluginid" : self.getId(),
                              })
        if kw.get('fullname'):
            users = ploneapi.content.find(portal_type='Benutzer', Title=kw.get('fullname'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})

        elif kw.get('email'):
            users = ploneapi.content.find(portal_type='Benutzer', mandant_email=kw.get('email'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})
        elif kw.get('name'):
            users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=kw.get('name'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})
        return mylist


    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):

        ticketmethod = ploneapi.portal.get_registry_record(name='ticketmethod', default=1)
        if ticketmethod == 1:
            return dict()

        if user:
            userid = user.getUserId()
            try:
                userbrains = ploneapi.content.find(portal_type='Benutzer', mandant_userid=userid)
            except:
                print('Error in encoding')
                userbrains = []
            if userbrains:
                logged = userbrains[0].getObject()
                mydict = {}
                mydict['fullname'] = logged.title
                mydict['email'] = logged.email
                if logged.location:
                    mydict['location'] = logged.location
                if logged.biography:
                    mydict['description'] = logged.biography
                return mydict
        return dict()

    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None, attr=None):
        if not request:
            return ()
        try:
            ticketdomain = api.portal.get_registry_record('ticketdomain')
            ticketgroup = api.portal.get_registry_record('ticketgroup')
        except:
            return ()
        if ticketdomain and ticketgroup:
            if principal.getProperty('email').endswith(ticketdomain):
                return [ticketgroup]
        users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=principal.getId())
        if users:
            try:
                userobj = users[0].getObject()
                return [userobj.aq_parent.group]
            except:
                return () 
        return () 

InitializeClass(EdiTicketAuth)
