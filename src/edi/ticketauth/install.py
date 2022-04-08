from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_editicketauth_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_editicketauth_form' )


def manage_add_editicketauth_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add an editicket Helper to the PluggableAuthentication Service."""

    sp = plugin.EdiTicktAuth( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'inwimandantHelper+added.'
                                      % dispatcher.absolute_url() )


def register_editicketauth_plugin():
    registerMultiPlugin(plugin.EdiTicketAuth.meta_type)


def register_editicketauth_plugin_class(context):
    context.registerClass(plugin.EdiTicketAuth,
                          permission = manage_users,
                          constructors = (manage_add_editicketauth_form,
                                          manage_add_editicketauth_helper),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
