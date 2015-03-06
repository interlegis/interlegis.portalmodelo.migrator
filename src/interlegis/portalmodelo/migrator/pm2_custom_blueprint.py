from collections import defaultdict
import posixpath

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from zope.interface import classProvides, implements
from collective.jsonmigrator import logger


class PM2CustomBlueprint(object):

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        types = defaultdict(list)
        type_substitution = {
            'Large Plone Folder': 'Folder',
        }
        for item in self.previous:
            path = item['_path']
            # skip
            if posixpath.basename(path.strip('/')) in {'syndication_information',
                                                       'crit__created_ATSortCriterion',
                                                       'crit__Type_ATPortalTypeCriterion'}:
                logger.info(':: SKIPPED -> ' + path)
                continue
            item['_path'] = path.replace('cm_flo/portal', 'novo')

            original_type = item['_type']
            item['_type'] = type_substitution.get(original_type, original_type)

            # DEV
            types[original_type].append(path)

            yield item

        print '##################################################################################'
        print '##################################################################################'
        print '##################################################################################'
        for k, l in types.iteritems():
            print 'VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV'
            print k
            print '----------------------------------------------------------------------------------'
            print l
        print '##################################################################################'
        print '##################################################################################'
        print '##################################################################################'
        print types.keys()
