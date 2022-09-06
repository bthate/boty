# jsb/imports.py
#
#

""" provide a import wrappers for the contrib packages. """

## lib imports

from jsb.lib.jsbimport import _import

## basic imports

import logging

## getdns function

def getsleekxmpp():
    try:
        mod = _import("sleekxmpp")
    except: mod = _import("boty.contrib.sleekxmpp")
    logging.debug("imports - sleekxmpp module is %s" % str(mod))
    return mod
