# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.ticketauth -t test_ticket.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.ticketauth.testing.EDI_TICKETAUTH_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/ticketauth/tests/robot/test_ticket.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Ticket
  Given a logged-in site administrator
    and an add Ticket form
   When I type 'My Ticket' into the title field
    and I submit the form
   Then a Ticket with the title 'My Ticket' has been created

Scenario: As a site administrator I can view a Ticket
  Given a logged-in site administrator
    and a Ticket 'My Ticket'
   When I go to the Ticket view
   Then I can see the Ticket title 'My Ticket'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Ticket form
  Go To  ${PLONE_URL}/++add++Ticket

a Ticket 'My Ticket'
  Create content  type=Ticket  id=my-ticket  title=My Ticket

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Ticket view
  Go To  ${PLONE_URL}/my-ticket
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Ticket with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Ticket title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
