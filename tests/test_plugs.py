# tests/test_persist.py
#
#

""" tests for the persist module, the part of jsonbot that manages the data. """

## jsb imports

from jsb.lib.factory import bot_factory
from jsb.lib.datadir import getdatadir
from jsb.lib.boot import boot
from jsb.tests import JSBTest

## basic imports

import unittest
import os
import uuid
import logging
import time
import thread

## defines

booted = False

## locks

#lock = thread.allocate_lock()
#locked = lockdec(lock)

## class TestPersist

class TestPlugs(JSBTest):

    def setUp(self): 
        from jsb.utils.log import setloglevel
        setloglevel("error")
        JSBTest.setUp(self)
        self.uuid = str(uuid.uuid4())
        self.bot = bot_factory.create("console")
        try: self.bot.users.add('test', ['test@test', ], ['OPER', 'USER', 'QUOTE', 'MAIL', 'GUEST', "TEST"])
        except Exception, ex: pass   
        self.event = self.bot.make_event("test@test", "#test", "init")
        self.event.bind(self.bot)
        self.bot.cc = ";"

    def test_plugsexamples(self):
        global booted
        if not booted: boot(force=True) ; booted = True
        from jsb.plugs.core.test import dotest
        from jsb.utils.log import setloglevel
        setloglevel("info")
        dotest(self.bot, self.event, direct=True)
        from jsb.utils.exception import exceptionlist
        if exceptionlist: logging.error("exceptionlist is: %s" % str(exceptionlist))
        self.assertTrue(not exceptionlist)
