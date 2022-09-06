# tests/test_persist.py
#
#

""" tests for the persist module, the part of jsonbot that manages the data. """

## jsb imports

from jsb.utils.lazydict import LazyDict
from jsb.lib.datadir import getdatadir
from jsb.lib.persist import Persist, PersistCollection, findfilenames, needsaving
from jsb.lib.threads import start_new_thread
from jsb.lib.boot import boot
from jsb.utils.locking import lockdec
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

lock = thread.allocate_lock()
locked = lockdec(lock)

## class TestPersist

class TestPersist(JSBTest):

    def setUp(self): 
        JSBTest.setUp(self)
        self.uuid = str(uuid.uuid4())
        self.default = Persist("testdata" + os.sep + "test.default.%s" % self.uuid)

    def test_load(self):
        self.assertTrue(type(self.default) == Persist)

    def test_save(self):
        self.default.data.testdata = "this is a test sample %s" % self.uuid
        self.default.save()
        b = Persist("testdata" + os.sep + "test.default.%s" % self.uuid)
        self.assertTrue(b.data.testdata == "this is a test sample %s" % self.uuid)

    def test_defaultislazydict(self):
        self.assertTrue(type(self.default.data) == LazyDict)

    def test_threadedsave(self):
        threads = []
        for i in range(100):
            threads.append(start_new_thread(self.test_save, ()))
        for thr in threads: thr.join()
        b = Persist("testdata" + os.sep + "test.default.%s" % self.uuid)
        self.assertTrue(b.data.testdata == "this is a test sample %s" % self.uuid)

    def test_threadedsaveinline(self):
        threads = []
        totalcount = 0 
        c = Persist("testdata" + os.sep + "test.default.%s" % self.uuid)
        c.data.counter = 0
        c.save()
        @locked
        def save(counter):
            b = Persist("testdata" + os.sep + "test.default.%s" % self.uuid)
            if not b.data.counter: b.data.counter = 0
            b.data.counter += counter
            b.save()
        for i in range(100):
            totalcount += i
            threads.append(start_new_thread(save, (i,)))
        for thr in threads: thr.join()
        global needsaving
        while needsaving: time.sleep(0.1)
        time.sleep(1)
        logging.warn("%s - %s" % (c.data.counter, totalcount))
        self.assertTrue(c.data.counter == totalcount)
        
    def test_getfromlocalcache(self):
        self.default.data.testdata = "this is a test sample %s" % self.uuid
        a = self.default.get()
        logging.warn("get() returned %s" % a.tojson())
        self.assertTrue(a.testdata == "this is a test sample %s" % self.uuid)

    def test_persistcollectionnames(self): 
        if not booted: boot(force=True)
        a = PersistCollection(getdatadir() + os.sep + "run")
        logging.warn(str(a.names()))
        self.assertTrue("cmndtable" in a.names())

    def test_persistcollectionobjects(self):
        if not booted: boot(force=True)
        a = PersistCollection(getdatadir() + os.sep + "run")
        objects = a.objects("cmndtable").items()
        logging.warn(str(objects))
        self.assertTrue("list" in objects[0][1].data)
