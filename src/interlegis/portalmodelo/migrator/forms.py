from collective.jsonmigrator import msgFact as _, logger
from collective.transmogrifier.transmogrifier import Transmogrifier
from plone.z3cform.layout import wrap_form
from z3c.form import button, field, form
from zope.interface import Interface
from zope.schema import ASCIILine, TextLine, URI


class IPortalModeloMigrator(Interface):

    remote_url = URI(
        title=_(u"URL"),
        description=_(u"URL for the remote portal modelo 2 to migrate"),
        required=True,
    )

    remote_username = ASCIILine(
        title=_(u"Username"),
        description=_(u"Username to log in to the remote site"),
        required=True,
    )

    remote_password = TextLine(
        title=_(u"Password"),
        description=_(u"Password to log in to the remote site"),
        required=True,
    )

    remote_path = TextLine(
        title=_(u"Start path"),
        description=_(u"Path where to start crawling and importing"),
        required=True,
    )


class PortalModeloMigrator(form.Form):

    label = _(u"Migrate from Portal Modelo 2")
    fields = field.Fields(IPortalModeloMigrator)
    ignoreContext = True

    @button.buttonAndHandler(u'Run')
    def handleRun(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        overrides = {'remotesource': {k.replace('_', '-'): v for k, v in data.iteritems()}}
        logger.info("Start of importing")
        Transmogrifier(self.context)('interlegis.portalmodelo.migrator', **overrides)
        logger.info("End of importing")


PortalModeloMigratorView = wrap_form(PortalModeloMigrator)
