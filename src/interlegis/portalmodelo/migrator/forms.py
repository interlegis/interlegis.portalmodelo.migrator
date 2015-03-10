import logging
from StringIO import StringIO

from Products.Five.browser import BrowserView
from collective.jsonmigrator import msgFact as _, logger
from plone.z3cform.layout import wrap_form
from z3c.form import button, field, form
from zope.interface import Interface
from zope.schema import ASCIILine, TextLine, URI, Password

from pm2_migration import run_migration


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

    remote_password = Password(
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

        log_output = StringIO()
        logHandler = logging.StreamHandler(log_output)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)

        run_migration(self.context, overrides)

        logHandler.flush()
        log_output.flush()
        session = self.request.SESSION
        session['log'] = log_output.getvalue()

        self.request.RESPONSE.redirect('/'.join((self.context.absolute_url(), '@@migrate_result')))


PortalModeloMigratorView = wrap_form(PortalModeloMigrator)


class PortalModeloMigratorResultView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        session = self.request.SESSION
        log = session['log']
        msgs = [l for l in log.split('\n') if ' - INFO - :: Skipping -> ' not in l]

        actually_skipped = [a.split(' -> ')[-1] for a in msgs if 'ACTUALLY SKIPPED -> ' in a]
        filtered_msgs = [l for l in msgs if all(a not in l for a in actually_skipped)]

        return '\n'.join(filtered_msgs)
