# jsb/db/__init__.py
#
#

""" main db package """

## jsb imports

from jsb.utils.exception import handle_exception

## basic imports

import logging

## gotsqlite function

def gotsqlite():
    try: import _sqlite3 ; return True
    except ImportError: return False

## getmaindb function

db = None

def getmaindb():
    try:
        from jsb.lib.config import getmainconfig
        cfg = getmainconfig()
        if cfg.dbenable:
            if "sqlite" in cfg.dbtype and not gotsqlite():
                logging.error("sqlite is not found.")
                return
            global db
            if db: return db
            from direct import Db
            return Db()
    except Exception, ex: handle_exception()
