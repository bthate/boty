# boty/drivers/xmpp/bot.py
#
#

""" XMPP bot build on sleekxmpp. """

## boty imports

from boty.imports import getsleekxmpp

sleekxmpp = getsleekxmpp()

## jsb imports

from jsb.utils.xmpp import stripped
from jsb.lib.botbase import BotBase
from boty.drivers.xmpp.message import Message

## basic imports

import logging

## BotyXMPPBot class

class BotyXMPPBot(BotBase):

    def __init__(self, cfg, name="boty-xmpp"):
        BotBase.__init__(self, cfg, name=name)
        self.xmpp = sleekxmpp.clientxmpp.ClientXMPP(cfg.user, cfg.password)
        self.xmpp.add_event_handler("session_start", self.session_start)
        self.xmpp.add_event_handler("message", self.message)
        if cfg.openfire:
            import ssl
            self.xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    def start(self, connect=True):
        BotBase.start(self, connect=False)
        if connect: self.xmpp.connect()
        self.xmpp.process()

    def session_start(self, event):
        self.xmpp.send_presence()

    def send(self, event):
        try:
            xml = event.tojabber()
            if not xml:
                raise Exception("can't convert %s to xml .. bot.send()" % what)
        except (AttributeError, TypeError):
            handle_exception()
            return
        self.xmpp.send_raw(xml)

    def outnocb(self, printto, txt, how=None, event=None, html=False, isrelayed=False, *args, **kwargs):
        """ output txt to bot. """
        #if printto and printto in self.state['joinedchannels']: outtype = 'groupchat'
        #else: outtype = "chat"
        target = printto
        txt = self.normalize(txt)
        #txt = stripcolor(txt)
        repl = Message(event)
        repl.to = target
        repl.type = (event and event.type) or "chat"
        repl.txt = txt
        if html:
            repl.html = txt
        logging.debug("%s - reply is %s" % (self.cfg.name, repl.dump()))
        if not repl.type: repl.type = 'normal'
        logging.debug("%s - sxmpp - out - %s - %s" % (self.cfg.name, printto, unicode(txt)))
        self.send(repl)

    def message(self, data):
        """ message handler. """   
        m = Message()
        m.parse(data, self)
        if m.type == 'groupchat' and m.subject:
            logging.debug("%s - checking topic" % self.cfg.name)
            self.topiccheck(m)
            nm = Message(m)   
            callbacks.check(self, nm)
            return
        if m.isresponse:
            logging.debug("%s - message is a response" % self.cfg.name)
            return
        jid = None
        m.origjid = m.jid
        if self.cfg.user in m.jid or (m.groupchat and self.cfg.nick == m.nick):
            logging.debug("%s - message to self .. ignoring" % self.cfg.name)
            return 0
        if self.cfg.fulljids and not m.msg:
            utarget = self.userhosts.get(m.nick)
            if utarget: m.userhost = m.jid = m.auth = stripped(utarget)
            else: m.userhost = m.jid
        if m.msg: m.userhost = stripped(m.userhost)
        logging.debug("using %s as userhost" % m.userhost)
        m.dontbind = False
        self.put(m)
        



