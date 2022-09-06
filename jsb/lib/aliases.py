# jsb/lib/aliases.py
#
#

""" global aliases. """

## jsb imports

from jsb.lib.datadir import getdatadir

## basic imports

import os

aliases = None

## getaliases function

def getaliases(ddir=None, force=True):
    """ return global aliases. """
    global aliases
    if not aliases or force:
        from jsb.lib.persist import Persist
        from jsb.utils.lazydict import LazyDict
        d = ddir or getdatadir()
        p = Persist(d + os.sep + "aliases")
        if not p.data: p.data = LazyDict()
        aliases = p.data
    return aliases

def savealiases(ddir=None):
    """ return global aliases. """
    global aliases
    if aliases:
        from jsb.lib.persist import Persist
        from jsb.utils.lazydict import LazyDict
        d = ddir or getdatadir()
        p = Persist(d + os.sep + "aliases")
        p.data = aliases
        p.save()
    return aliases

def size():
    return len(aliases)

def setalias(first, second):
    a = getaliases()
    a[first] = second
