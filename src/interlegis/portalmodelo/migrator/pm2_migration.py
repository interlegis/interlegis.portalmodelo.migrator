import posixpath

from Products.CMFCore.utils import getToolByName
from collective.jsonmigrator import logger
from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier
from zope.interface import classProvides, implements


class PM2CustomBlueprint(object):

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        type_substitution = {
            'Large Plone Folder': 'Folder',
        }
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
            item['_path'] = path.replace('cm_flo/portal', 'institucional')

            # Adjust types
            original_type = item['_type']
            item['_type'] = type_substitution.get(original_type, original_type)

            # Change all workflows to 'simple_publication_workflow'
            if '_workflow_history' in item:
                values = item['_workflow_history'].values()
                # There should be exactly one key, value pair. We discard the key
                assert len(values) == 1
                item['_workflow_history'] = {'simple_publication_workflow': values[0]}

            yield item


def run_migration(context, overrides):
    logger.info("Start of importing")

    Transmogrifier(context)('interlegis.portalmodelo.migrator', **overrides)

    wf_tool = getToolByName(context, 'portal_workflow')
    wf_tool.updateRoleMappings()

    catalog = getToolByName(context, 'portal_catalog')
    catalog.clearFindAndRebuild()

    logger.info("End of importing")
