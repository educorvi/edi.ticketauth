# edi.ticketauth

Das Plugin edi.ticketauth verfolgt das Ziel, die Schwelle für die Nutzung eines Portalangebotes zu reduzieren ohne die Sicherheit
bedeutend einzuschränken. Allein die Verwendung von Benutzername + Kennwort für die Anmeldung hat sich bei gelegentlich genutzten 
Online-Portalen als zu hohe Barriere für Benutzer erwiesen. Eine strenge Passwort-Policy, verbunden mit dem aufwendigen Verfahren 
bei "Passwort vergessen" hat bei Benutzern zur Nicht-Nutzung eines Online-Angebotes geführt.

Mit edi.ticketauth können Benutzer jederzeit spontan ein Login-Ticket per E-Mail anfordern. Das Login-Ticket besteht aktuell aus 
einem 6-stelligen Zahlencode. Das Login-Ticket wird per E-Mail an die im System hinterlegte E-Mail-Adresse ausgeliefert. Das Ticket 
hat eine begrenzte Gültigkeit, die vom Adminstrator eingestellt werden kann. Das Ticket wird im Homefolder des Benutzers gespeichert. 
Das Ticket kann alternativ zum hinterlegten Passwort verwendet werden. Das Passwort behält weiterhin seine Gültigkeit.

edi.ticketauth verfügt über eine API-Schnittstelle damit es auch von Drittanwendungen (z.B. beim Versand von Erinnerungs-E-Mails)
verwendet werden kann. Außerdem können Administratoren Ticketlisten zum Massenversand via Post oder E-Mail erzeugen.

**Achtung: edi.ticketauth darf momentan nicht verwendet werden, wenn über die Anwendung die Rechte natürlicher Personen betroffen sind
und dementsprechend für die Anwendung eine Datenschutz-Folgenabschätzung erstellt werden muss. Insofern darf edi.ticketauth ausdrücklich
nicht verwendet werden, wenn über die Anwendung Sozialdaten veröffentlicht werden.**

## Leistungsmerkmale

- Anforderung eines Tickets durch den Benutzer `(BrowserView: /@@newticket)`
- Content-Type "Ticket" zur Speicherung von Tickets im Homefolder der Benutzer
- PAS-Plugin zur Authentisierung von Benutzern auf Basis der Tickets im Homefolder
- Adminstrativer Browserview zum nachträglichen Anlegen der Homefolder `(BrowserView: /@@create-homefolders)`
- Adminsitrativer Browserview zum Anlegen von Tickets zum Massenversand `(BrowserView: /@@create-tickets)`
- RESTful API für Drittanwendungen zur Erzeugung von Tickets (z. B. bei Erinnerungs E-Mails)
- Controlpanel (Einstellungen für edi.ticketauth: `/@@editicket-controlpanel`)


## Dokumentation

### Benutzer

Benutzer können über die URL `/@@newticket` jederzeit spontan ein neues Ticket anfordern. Das Ticket wird über E-Mail versendet.

### Admins

- Admins können über das Controlpanel: `/@@editicket-controlpanel` Einstellungen für edi.ticketauth vornehmen.
- Admins können über den Browserview: `/@@create-homefolders` nachträglich Benutzerordner anlegen.
- Admins können über den Browserview: `/@@create-tickets` Tickets für den Massenversand erzeugen.

### API

```
import requests
from plone import api as ploneapi

ticketlogin = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.ticketlogin')
ticketpassword = ploneapi.portal.get_registry_record('edi.ticketauth.configpanel.IEdiTicketSettings.ticketpassword')
login = {'login': ticketlogin, 'password': ticketpassword}
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
authtoken = requests.post(self.authurl, headers=headers, json=login)
payload = {'email': email} # E-Mail muss beim Aufruf übergeben werden
reqheaders = {'Accept': 'application/json','Authorization': 'Bearer %s' % authtoken}
result = requests.get(url, params=payload, headers=headers, verify=False)
resultdata = result.json()
ticket = {'status':'success', 'ticket':resultdata.get('ticket')}

```

## Übersetzung

Das Add-On ist derzeit nur auf Deutsch verfügbar.

## Installation

Installation von edi.ticketauth durch Hinzufügen zur buildout.cfg:

```
    [buildout]

    ...

    eggs =
        edi.ticketauth
```

Danach Ausführung von: `bin/buildout`

- Das Add-On edi.ticketauth muss nach dem Neustart des Servers im Plone Controlpanel installiert werden.
- Es muss ein Benutzer angelegt und mit allen notwendigen Rechten ausgestattet werden, um in den Benutzerordnern Tickets anzulegen.
- Im Controlpanel von edi.ticketauth müssen die notwendigen Einstellungen getroffen werden.  
- Nach erfolgreicher Plone-Installation muss das PAS-Plugin über das Zope-Management-Interface (acl_users --> Add EdiTicketAuth) hinzugefügt
 und aktviert werden.
- Über die Sicherheitseinstellungen des Plone Controlpanels muss die Option "Persönliche Benutzerordner" aktiviert werden. 

## Alternative Authentifizierung für Mandanten

edi.ticketauth kann auch für die Authentifizierung von Mandanten genutzt werden. Dazu können in der Registry folgende Einträge gemacht werden:

ticketmethod = 1|2 1 - Ticketauthentifizierung | 2 - Authentifizierung über Mandanten
ticketdomain = subdomain.toplevel
ticketgroup = ID der Gruppe

Funktionsweise: wenn die E-Mail-Adresse der Benutzer:in auf die Ticketdomain endet wird die Benutzer:in der entsprechenden Gruppe zugeordnet

## Quellen

- Issue Tracker: https://github.com/educorvi/edi.ticketauth/issues
- Source Code: https://github.com/educorvi/edi.ticketauth


## Support

- Seppo Walther (seppo.walther@educorvi.de)
- Lars Walther (lars.walther@educorvi.de)


## Lizenz

MIT Lizenz
