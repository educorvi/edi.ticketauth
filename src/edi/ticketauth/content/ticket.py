from datetime import datetime
from datetime import timedelta
from plone import api as ploneapi
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

import random


def titlefactory():
    return "Ticket " + datetime.now().strftime("%d.%m.%Y.%H.%M.%S")


def ticketfactory():
    return str(random.randrange(100000, 999999))


def validfactory():
    validtime = ploneapi.portal.get_registry_record(
        "edi.ticketauth.configpanel.IEdiTicketSettings.validtime"
    )
    return datetime.now() + timedelta(days=validtime)


class ITicket(model.Schema):
    """Marker interface and Dexterity Python Schema for Ticket"""

    title = schema.TextLine(title="Titel", defaultFactory=titlefactory)
    ticket = schema.TextLine(title="Ticket", defaultFactory=ticketfactory)
    valid = schema.Datetime(title="gültig bis", defaultFactory=validfactory)


@implementer(ITicket)
class Ticket(Item):
    """ """
