from fabric import api
import os

def postdeploy():
    """ Send Apache config file to host
    """
    name = "ApacheRewrite.conf"
    tmp = os.path.join('/tmp', name)
    tgt = os.path.join(api.env.path, name)
    buildout = api.env['buildout-user']
    api.put(name, tmp)
    api.sudo("mv -f %(tmp)s %(tgt)s && "
                    "chown %(buildout)s %(tgt)s && "
                    "chmod a+r %(tgt)s" % locals() )
    return True
