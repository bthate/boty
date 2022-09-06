# jsb/imports.py
#
#

""" provide a import wrappers for the contrib packages. """

## lib imports

from lib.jsbimport import _import

## basic imports

import logging

## getdns function

def getdns():
    try:
        mod = _import("dns")
    except: mod = _import("jsb.contrib.dns")
    logging.debug("imports - dns module is %s" % str(mod))
    return mod

def getwebapp2():
    try:
        mod = _import("webapp2")
    except: mod = _import("jsb.contrib.webapp2")
    logging.debug("imports - webapp2 module is %s" % str(mod))
    return mod

## getjson function

def getjson():
    try:
        import wave
        #mod = _import("jsb.contrib.simplejson")
        mod = _import("json")
    except ImportError:
        try: mod = _import("json")
        except:
            try:
                mod = _import("simplejson")
            except:
                mod = _import("jsb.contrib.simplejson")
    logging.debug("imports - json module is %s" % str(mod))
    return mod

## getfeedparser function

def getfeedparser():
    try: mod = _import("feedparser")
    except: mod = _import("jsb.contrib.feedparser")
    logging.info("imports - feedparser module is %s" % str(mod))
    return mod

def getoauth():
    try: mod = _import("oauth")
    except:
        mod = _import("jsb.contrib.oauth")
    logging.info("imports - oauth module is %s" % str(mod))
    return mod

def getrequests():
    try: mod = _import("requests")
    except: mod = _import("jsb.contrib.requests")
    logging.info("imports - requests module is %s" % str(mod))
    return mod

def gettornado():
    try: mod = _import("tornado")
    except: mod = _import("jsb.contrib.tornado")
    logging.info("imports - tornado module is %s" % str(mod))
    return mod

def getBeautifulSoup():
    try: mod = _import("BeautifulSoup")
    except: mod = _import("jsb.contrib.BeautifulSoup")
    logging.info("imports - BeautifulSoup module is %s" % str(mod))
    return mod

def gethapi():
    try: mod = _import("hapi")
    except: mod = _import("jsb.contrib.hapi")
    logging.info("imports - hapi module is %s" % str(mod))
    return mod
