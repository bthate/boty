# jsb/boot.py
#
#

""" admin related data and functions. """

## basic imports

import logging
import os
import sys

## paths

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + os.sep + '..')

## defines

def boot(*args, **kwargs):
    logging.warn("BOTY BOOT")
    import jsb.utils.trace
    jsb.utils.trace.stopmarkers.append("boty")
    import jsb.lib.boot 
    jsb.lib.boot.plugin_packages.extend(['boty.plugs'])
    jsb.lib.boot.default_plugins.append("boty.plugs.version")
    logging.warn("booting with %s" % str(jsb.lib.boot.plugin_packages))
    jsb.lib.boot.boot(*args, **kwargs)
