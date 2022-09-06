# jsb/plugins.py
#
#

""" holds all the plugins. plugins are imported modules. """

## jsb imports

from thread import start_new_thread
from commands import cmnds
from callbacks import callbacks, remote_callbacks, first_callbacks, last_callbacks
from eventbase import EventBase
from persist import Persist
from jsb.utils.lazydict import LazyDict
from jsb.utils.exception import handle_exception
from boot import cmndtable, plugin_packages, default_plugins
from errors import NoSuchPlugin, URLNotEnabled
from jsb.utils.locking import lockdec
from jsbimport import force_import, _import
from morphs import outputmorphs, inputmorphs
from wait import waiter
from boot import plugblacklist

## basic imports

import os
import logging
import Queue
import copy
import sys
import thread
import types
import time
from collections import deque

## defines

cpy = copy.deepcopy

## locks

loadlock = thread.allocate_lock()
locked = lockdec(loadlock)

## Plugins class

class Plugins(LazyDict):

    """ the plugins object contains all the plugins. """

    loading = LazyDict()

    def size(self): return len(self)

    def exit(self):
        todo = cpy(self)
        for plugname in todo:
            self.unload(plugname)         

    def reloadfile(self, filename, force=True):
        logging.warn("plugs - reloading file %s" % filename)
        mlist = filename.split(os.sep)
        mod = []
        for m in mlist[::-1]:
            mod.insert(0, m)
            if m == "myplugs": break 
        modname = ".".join(mod)[:-3]
        from boot import plugblacklist
        if modname in plugblacklist.data: logging.warn("%s is in blacklist .. not loading." % modname) ; return
        logging.warn("plugs - using %s" % modname)
        self.reload(modname, force)
          
    def loadall(self, paths=[], force=True):
        """
            load all plugins from given paths, if force is true .. 
            otherwise load all plugins for default_plugins list.

        """
        if not paths: paths = plugin_packages
        imp = None
        for module in paths:
            try: imp = _import(module)
            except ImportError, ex:
                #handle_exception()
                logging.warn("no %s plugin package found - %s" % (module, str(ex)))
                continue
            except Exception, ex: handle_exception()
            logging.debug("got plugin package %s" % module)
            try:
                for plug in imp.__plugs__:
                    mod = "%s.%s" % (module, plug)
                    try: self.reload(mod, force=force, showerror=True)
                    except KeyError: logging.debug("failed to load plugin package %s" % module)
                    except Exception, ex: handle_exception()
            except AttributeError: logging.error("no plugins in %s .. define __plugs__ in __init__.py" % module)

    def unload(self, modname):
        """ unload plugin .. remove related commands from cmnds object. """
        logging.debug("plugins - unloading %s" % modname)
        try:
            self[modname].shutdown()
            logging.debug('called %s shutdown' % modname)
        except KeyError:
            logging.debug("no %s module found" % modname) 
            return False
        except AttributeError: pass
        try: cmnds.unload(modname)
        except KeyError: pass
        try: first_callbacks.unload(modname)
        except KeyError: pass
        try: callbacks.unload(modname)
        except KeyError: pass
        try: last_callbacks.unload(modname)
        except KeyError: pass
        try: remote_callbacks.unload(modname)
        except KeyError: pass
        try: outputmorphs.unload(modname)
        except: handle_exception()
        try: inputmorphs.unload(modname)
        except: handle_exception()
        try: waiter.remove(modname)
        except: handle_exception()
        return True

    def load(self, modname, force=False, showerror=True, loaded=[]):
        """ load a plugin. """
        if not modname: raise NoSuchPlugin(modname)
        if not force and modname in loaded: logging.warn("skipping %s" % modname) ; return loaded
        from boot import plugblacklist
        if plugblacklist and modname in plugblacklist.data: logging.warn("%s is in blacklist .. not loading." % modname) ; return loaded
        if self.has_key(modname):
            try:
                logging.debug("%s already loaded" % modname)                
                if not force: return self[modname]
                self[modname] = reload(self[modname])
            except Exception, ex: raise
        else:
            logging.debug("trying %s" % modname)
            mod = _import(modname)
            if not mod: return None
            try: self[modname] = mod
            except KeyError:
                logging.info("failed to load %s" % modname)
                raise NoSuchPlugin(modname)
        try: init = getattr(self[modname], 'init')
        except AttributeError: init = None
        try: threaded_init = getattr(self[modname], 'init_threaded')
        except AttributeError: threaded_init = None
        try:
            init and init()
            logging.debug('%s init called' % modname)
        except URLNotEnabled: logging.error("URL fetching is disabled")
        except Exception, ex: raise
        try:
            threaded_init and start_new_thread(threaded_init, ())
            logging.debug('%s threaded_init started' % modname)
        except Exception, ex: raise
        logging.warn("%s loaded" % modname)
        return self[modname]

    def loaddeps(self, modname, force=False, showerror=False, loaded=[]):
        if not "." in modname: modname = self.getmodule(modname)
        if not modname: logging.error("no modname found for %s" % modname) ; return []
        try:
            deps = self[modname].__depending__
            if deps: logging.warn("dependcies detected: %s" % deps)
        except (KeyError, AttributeError): deps = []
        deps.insert(0, modname)
        for dep in deps:
            if dep not in loaded:
                self.loading[dep] = time.time()
                if self.has_key(dep): self.unload(dep)
                try:
                    self.load(dep, force, showerror, loaded)
                    loaded.append(dep)
                except Exception, ex: del self.loading[dep] ; raise
                self.loading[dep] = 0 
        return loaded

    def reload(self, modname, force=False, showerror=False):
        """ reload a plugin. just load for now. """ 
        if type(modname) == types.ListType: loadlist = modname
        else:
            loadlist = [modname, ]
        loaded = []
        for modname in loadlist:
            modname = modname.replace("..", ".")
            loaded.extend(self.loaddeps(modname, force, showerror, []))
        return loaded

    def fetch(self, plugname):
        mod = self.getmodule(plugname)
        if mod: self.reload(mod) ; return self.get(mod)

    def getmodule(self, plugname):
        for module in plugin_packages:
            try: imp = _import(module)
            except ImportError, ex:
                if "No module" in str(ex):
                    logging.info("no %s plugin package found" % module)
                    continue
                raise
            except Exception, ex: handle_exception() ; continue
            if plugname in imp.__plugs__: return "%s.%s" % (module, plugname)

## global plugins object

plugs = Plugins()
