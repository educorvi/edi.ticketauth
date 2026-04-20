from AccessControl.Permissions import add_user_folders
from edi.ticketauth.plugin import EdiTicketAuth
from edi.ticketauth.plugin import manage_addTicketPlugin
from edi.ticketauth.plugin import manage_addTicketPluginForm
from edi.ticketauth.plugin import zmidir
from Products.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory

import os


__version__ = "1.0.0a0"

PACKAGE_NAME = "edi.ticketauth"

_ = MessageFactory(PACKAGE_NAME)


def initialize(context):
    print("ediTicket " * 10)
    registerMultiPlugin(EdiTicketAuth.meta_type)
    context.registerClass(
        EdiTicketAuth,
        permission=add_user_folders,
        icon=os.path.join(zmidir, "user.png"),
        constructors=(manage_addTicketPluginForm, manage_addTicketPlugin),
        visibility=None,
    )
