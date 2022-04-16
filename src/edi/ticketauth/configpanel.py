# -*- coding: utf-8 -*-
from plone import schema
from z3c.form import form
from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface

defaultmailsubject = "Neues Login-Ticket"

defaultmailtext = """\
<p>Sehr geehrte(r) Frau/Herr {{ name }},</p>
<p>Sie haben ein neues Ticket für den Zugang zum Portal: {{ portalname }} angefordert.</p>
</p>Das neue Ticket ist {{ ticketgueltigkeit }} Tage gültig. Sie können Sie mit folgenden Daten am Portal anmelden:</p>
<p>Benutzername: {{ email }}<br/>
Passwort: <strong>{{ ticket }}</strong></p>
<p>Zur Anmeldung am Portal klicken Sie den folgenden Link:</p>
<p><a href="{{ portalurl }}">{{ portalurl }}</a></p>
<p>Mit freundlichen Grüßen<br/>
Ihre BG ETEM</p>"""

defaultformhelp = """\
Sie können hier ein neues Ticket anfordern. Sie erhalten das Ticket per E-Mail. Bitte schauen Sie auch
in Ihren SPAM-Ordner. Das Ticket hat eine Gültigkeit von einem Tag. Sie können das Ticket anstatt ihres
Passwortes verwenden."""

class IEdiTicketSettings(Interface):
    
    ticketlogin = schema.TextLine(title="Benutzer für das Anlegen von Tickets")

    ticketpassword = schema.Password(title="Passwort für den Benutzer")

    validtime = schema.Int(title="Gültigkeit des Tickets in Tagen", default=1)

    mailsubject = schema.TextLine(title="Betreff der E-Mail bei Anforderung eines neues Tickets", default=defaultmailsubject)

    mailtext = schema.Text(title="Text der E-Mail.",
                           description="Es können folgende Variablen verwendet werden: name, portalname, ticketgueltigkeit,\
                                        email, ticket, portalurl. Bitte schreiben Sie {{ variablenname }}.",
                           default=defaultmailtext)

    formhelp = schema.Text(title="Hilfetext für das Formular zur Anforderung eines neuen Tickets", default=defaultformhelp)

class EdiTicketPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IEdiTicketSettings

EdiTicketControlPanelView = layout.wrap_form(EdiTicketPanelForm, ControlPanelFormWrapper)
EdiTicketControlPanelView.label = u"Einstellungen edi.ticketauth"
