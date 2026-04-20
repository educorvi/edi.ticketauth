from edi.ticketauth.content.ticket import ticketfactory
from edi.ticketauth.content.ticket import titlefactory
from edi.ticketauth.content.ticket import validfactory
from plone import api as ploneapi
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides


class HomeFolders(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        userlist = ploneapi.user.get_users()
        mt = ploneapi.portal.get_tool(name="portal_membership")
        for user in userlist:
            mt.createMemberarea(member_id=user.getId())
        return self.index()


class TicketsForUsers(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        userlist = ploneapi.user.get_users()
        mt = ploneapi.portal.get_tool(name="portal_membership")
        ticketlist = []
        for user in userlist:
            memberfolder = mt.getHomeFolder(user.getId())
            if memberfolder:
                entry = {}
                ticketobject = ploneapi.content.create(
                    type="Ticket",
                    title=titlefactory(),
                    valid=validfactory(),
                    ticket=ticketfactory(),
                    container=memberfolder,
                )
                entry["name"] = user.getProperty("fullname")
                entry["email"] = user.getProperty("email")
                entry["ticket"] = ticketobject.ticket
                entry["valid"] = ticketobject.valid.strftime("%d.%m.%Y")
                ticketlist.append(entry)
        self.ticketlist = ticketlist
        return self.index()
