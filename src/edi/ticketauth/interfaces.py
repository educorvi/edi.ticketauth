# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.PluggableAuthService import interfaces


class IEdiTicketauthLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEdiTicketAuthPlugin(interfaces.plugins.IAuthenticationPlugin):
    pass
