# tests/test_sanity.py
#
#

""" tests to run on the sanitydata datadir. """

## jsb imports

from jsb.lib.plugins import plugs
from jsb.lib.persist import Persist, findfilenames
from jsb.lib.threads import start_new_thread
from jsb.tests import JSBTest

## basic imports
 
import unittest
import os
import uuid
import logging

## class TestSanity

class TestSanity(JSBTest):

    def setUp(self):
        JSBTest.setUp(self)
        self.uuid = str(uuid.uuid4())
        self.default = Persist("sanitydata" + os.sep + "test.sanity.%s" % self.uuid)
        if not self.default.data.sizes: self.default.data.sizes = {}

    def test_checksanityfilespersisted(self):
        errors = {}
        def loopfiles(dir):
            for i in findfilenames(dir):
                if i.endswith(".py") or i.endswith(".pyc"): continue
                if 'config' in i or 'upload' in i or 'data' in i or 'templates' in i or 'static' in i or 'run' in i: continue
                if os.path.isdir(dir + os.sep + i): loopfiles(dir + os.sep + i)
                else:
                    try:
                        b = Persist(dir + os.sep + i)
                        self.default.data.sizes[dir + os.sep + i] = len(b.data)
                    except Exception, ex: errors[dir + os.sep + i] = str(ex)
        loopfiles("sanitydata")
        if errors: logging.error(errors)
        self.assertTrue(not errors)
