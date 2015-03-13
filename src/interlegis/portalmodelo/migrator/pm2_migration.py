import posixpath

from Products.CMFCore.utils import getToolByName
from collective.jsonmigrator import logger
from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier
from zope.interface import classProvides, implements


TYPE_SUBSTITUTION = {
    'Large Plone Folder': 'Folder',
}


class PM2CustomBlueprint(object):

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.remote_path = str(options['remote-path'].strip('/'))
        self.destiny_path = str(options['destiny-path'].strip('/'))

    def __iter__(self):
        for item in self.previous:
            path = item['_path']

            # skip
            if posixpath.basename(path.strip('/')) in {'syndication_information',
                                                       'crit__created_ATSortCriterion',
                                                       'crit__Type_ATPortalTypeCriterion',
                                                       'lista-eventos',
                                                       'lista-noticias',
                                                       }:
                logger.info(':: ACTUALLY SKIPPED -> ' + path)
                continue

            # Rewrite path
            assert path.startswith(self.remote_path)
            item['_path'] = self.destiny_path + path[len(self.remote_path):]

            # Adjust types
            original_type = item['_type']
            item['_type'] = TYPE_SUBSTITUTION.get(original_type, original_type)

            # Change all workflows to 'simple_publication_workflow'
            if '_workflow_history' in item:
                values = item['_workflow_history'].values()
                if values:
                    # There should be exactly one key, value pair, if any. We change the key
                    assert len(values) == 1
                    item['_workflow_history'] = {'simple_publication_workflow': values[0]}

            # rename content with id == 'index_html' to just 'index'
            container, id = posixpath.split(item['_path'].strip('/'))
            if id == 'index_html':
                item['_path'] = '/'.join((container, 'index'))

            yield item


def run_migration(context, overrides):
    logger.info("Start of importing")

    Transmogrifier(context)('interlegis.portalmodelo.migrator', **overrides)

    wf_tool = getToolByName(context, 'portal_workflow')
    wf_tool.updateRoleMappings()

    catalog = getToolByName(context, 'portal_catalog')
    catalog.clearFindAndRebuild()

    logger.info("End of importing")
