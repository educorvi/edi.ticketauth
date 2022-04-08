# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# lwalther@novareto.de
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from OFS.Cache import Cacheable
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

import interfaces

from base64 import encodestring, decodestring
from urllib import quote, unquote
from plone import api as ploneapi

import logging

logger = logging.getLogger('edi.EdiTicketAuth')


class EdiTicketAuth(BasePlugin, Cacheable):
    """Multi-plugin
    """

    meta_type = 'EdiTicketAuth'
    security = ClassSecurityInfo()
    _dont_swallow_my_exceptions = True

    manage_options = ( ( { 'label': 'Users',
                           'action': 'manage_users', }
                         ,
                       )
                     + BasePlugin.manage_options
                     + Cacheable.manage_options
                     )

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        login = credentials.get( 'login' )
        password = credentials.get( 'password' )
        if login is None or password is None:
            return None
        import pdb;pdb.set_trace()
        return None


classImplements(EdiTicketAuth, interfaces.IEdiTicketAuth)
InitializeClass(EdiTicketAuth)
