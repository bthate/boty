# jsb/tests/__init__.py
#
#

""" define core test classes. """

## basic imports

import unittest

## class TestPersist

class JSBTest(unittest.TestCase):  

    def setUp(self):
        try:
            from google.appengine.api import memcache
            from google.appengine.ext import db
            from google.appengine.ext import testbed
            self.testbed = testbed.Testbed()
            self.testbed.activate() 
            self.testbed.init_datastore_v3_stub()
            self.testbed.init_memcache_stub()
        except ImportError: self.testbed = None

    def tearDown(self):
        if self.testbed: self.testbed.deactivate()
