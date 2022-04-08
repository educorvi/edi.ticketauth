# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer

from datetime import datetime
from datetime import timedelta
import random

# from edi.ticketauth import _


def titlefactory():
    return 'Ticket '+datetime.now().strftime("%d.%m.%Y.%H.%M.%S")

def ticketfactory():
    return str(random.randrange(100000, 999999)) 

def validfactory():
    return datetime.now() + timedelta(days=21)


class ITicket(model.Schema):
    """ Marker interface and Dexterity Python Schema for Ticket
    """

    title = schema.TextLine(title=u'Titel', defaultFactory=titlefactory)
    ticket = schema.TextLine(title=u'Ticket', defaultFactory=ticketfactory)
    valid = schema.Datetime(title=u'gültig bis', defaultFactory=validfactory)

@implementer(ITicket)
class Ticket(Item):
    """
    """
