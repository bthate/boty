# jsb/version.py
#
#

""" version related stuff. """

## jsb imports

from jsb.lib.config import getmainconfig

## basic imports

import os
import binascii

## defines

version = "0.84.1"

## getversion function

def getversion(txt=""):
    """ return a version string. """
    return "JSONBOT %s RC2 %s" % (version, txt)
