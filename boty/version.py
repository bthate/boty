# boty/version.py
#
#

""" version related stuff. """

## defines

version = "0.1"

## getversion function

def getversion(txt=""):
    """ return a version string. """
    return "BOTY %s %s" % (version, txt)
