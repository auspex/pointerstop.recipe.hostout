# -*- coding: utf-8 -*-
"""Recipe hostout"""

from StringIO import StringIO
from pkg_resources import resource_filename
import ConfigParser

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.optionsfile = self.name+".cfg"
        self.options['fabfiles'] = '%s\n%s' % (resource_filename(__name__, 'fabfile.py'), self.options.get('fabfiles', ''))

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        supervisor = self.name
        buildout   = self.buildout
        host       = buildout[supervisor].get('host')
        sections   = [(int(buildout[x].get('port-base',0)),x) for x in buildout.keys() 
                        if x <> supervisor 
                        and buildout[x].get('recipe','') == 'collective.hostout'
                        and buildout[x].get('host','') == host 
                        ] 
        sections.sort()
        rules    = open('ApacheRewrite.conf', 'w+')
        programs = StringIO()
        events   = StringIO()
        print >>programs
        print >>events
        for key in sections:
            base    = key[0]
            name    = key[1]
            section = buildout[name]
            path = section.get('path')
            base = int(section.get('port-base',0))
            print >>programs, "%d %s %s/parts/zeo/bin/runzeo" % (base, name+"-zeo", path)
            print >>programs, "%d %s (startsecs=30) %s/parts/instance/bin/runzope" % (base+1, name+"-plone", path)
            print >>events,   ("HttpOk TICK_60 ${buildout:bin-directory}/httpok [-p %s-plone -m plone-%s@localhost http://localhost:%d/]" %
                               (name, name, 12000+base))

            config = ConfigParser.RawConfigParser()
            config.optionxform = str
            options = name+".cfg"
            config.read(options)
    
            if not config.has_section('instance'):
                config.add_section('instance')
            if not config.has_section('zeo'):
                config.add_section('zeo')
            config.set('instance', 'port-base',   str(base))
            config.set('zeo',      'zeo-address', str(base+12005))
            # last part of a hyhenated name, or whole name if there's no hyphen
            partName = name.upper()  
            storage = section.get('zeo-storage', partName)
            if not config.has_section('filestorage'):
                config.add_section('filestorage')
                config.add_section('filestorage_'+storage)
            config.set('filestorage', 'recipe', 'collective.recipe.filestorage')
            config.set('filestorage', 'parts',  storage)
            config.set('filestorage_'+storage, 'zeo-storage', storage.lower())
            fp = open(options, 'w+')
            config.write(fp)
            fp.close()

            port = base + 12000
            print >>rules, "RewriteRule ^/%(storage)s(.*) http://localhost:%(port)d/VirtualHostBase/http/www.marinebiodiversity.ca:80/%(storage)smount/VirtualHostRoot/%(storage)s$1 [L,P,NC]" % locals()
                
        
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read(self.optionsfile)

        if config.has_section('buildout'):
            installed = []
        else:
            config.add_section('buildout')
            installed = self.optionsfile
        if not config.has_section('supervisor'):
            config.add_section('supervisor')
        config.set('supervisor', 'recipe',  'collective.recipe.supervisor')
        config.set('supervisor', 'plugins', 'superlance')
        
        config.set('supervisor', 'programs',       programs.getvalue())
        config.set('supervisor', 'eventlisteners', events.getvalue())

        fp = open(self.optionsfile, 'w+')
        config.write(fp)
        fp.close()
        
        rules.close()
        programs.close()
        events.close()
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return installed

    def update(self):
        """Updater"""
        pass
