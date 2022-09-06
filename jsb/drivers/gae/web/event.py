# jsb/web/event.py
#
#

""" web event. """

## jsb imports

from jsb.lib.eventbase import EventBase
from jsb.utils.generic import splittxt, fromenc, toenc
from jsb.utils.xmpp import stripped
from jsb.lib.outputcache import add
from jsb.utils.url import getpostdata_gae
from jsb.utils.exception import handle_exception
from jsb.lib.channelbase import ChannelBase
from jsb.utils.lazydict import LazyDict
from jsb.imports import getjson

## gaelib imports

from jsb.utils.gae.auth import checkuser

## basic imports

import cgi
import logging
import re

## WebEvent class

class WebEvent(EventBase):

    def __init__(self, bot): 
        EventBase.__init__(self, bot=bot)
        self.bottype = "web"
        self.cbtype = "WEB"
        self.bot = bot
        self.nodispatch = False

    #def __deepcopy__(self, a):
    #    e = WebEvent(self)
    #    e.response = self.response
    #    e.request = self.request
    #    assert self.bot
    #    assert self.response
    #    assert self.request
    #    return e

    def parse(self, response, request):
        """ parse request/response into a WebEvent. """
        logging.warn("parsing %s" % request.body)
        body = getpostdata_gae(request)
        logging.warn("body is %s" % body)
        data = LazyDict(getjson().loads(body))
        self.target = data.target
        self.how = data.how
        if self.how == "undefined": self.how = "overwrite"
        logging.warn("web - how is %s" % self.how)
        input = data.cmnd
        self.isweb = True
        self.origtxt = fromenc(input.strip(), self.bot.encoding)
        self.txt = self.origtxt
        self.usercmnd = self.txt and self.txt.split()[0]
        self.groupchat = False
        self.response = response
        self.request = request
        (userhost, user, u, nick) = checkuser(response, request, self)
        self.userhost = fromenc(userhost)
        self.nick = fromenc(nick)
        self.auth = fromenc(userhost)
        self.stripped = stripped(self.auth)
        self.domain = None
        self.channel = stripped(userhost)
        logging.debug(u'web - parsed - %s - %s' % (self.txt, self.userhost)) 
        self.prepare(self.bot)
        assert self.bot
        assert self.response
        assert self.request
        return self

    def reply(self, txt, result=[], event=None, origin="", dot=u", ", nr=600, extend=0, *args, **kwargs):
        """ reply to this event """#
        if not txt: return
        if self.how == "background":
            txt = self.bot.makeoutput(self.channel, txt, result, origin=origin, nr=nr, extend=extend, *args, **kwargs)
            self.bot.outnocb(self.channel, txt, self.how, event=self, response=self.response, *args, **kwargs)
        else: self.bot.say(self.channel, txt, result, self.how, event=event or self, showall=True, *args, **kwargs)
        return self
