"""Module where all interfaces, events and exceptions live."""

from Products.PluggableAuthService import interfaces
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEdiTicketauthLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEdiTicketAuthPlugin(interfaces.plugins.IAuthenticationPlugin):
    pass
