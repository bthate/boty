# jsb/gae/web/bot.py
#
#

""" GAE web bot. """

## jsb imports

from jsb.utils.lazydict import LazyDict
from jsb.utils.exception import handle_exception
from jsb.lib.botbase import BotBase
from jsb.lib.outputcache import add
from jsb.utils.generic import toenc, fromenc, strippedtxt, stripcolor
from jsb.utils.url import re_url_match
from jsb.utils.timeutils import hourmin
from jsb.lib.channelbase import ChannelBase
from jsb.lib.container import Container
from jsb.imports import getjson
from jsb.lib.eventbase import EventBase
json = getjson()

## basic imports

import logging
import re
import cgi
import urllib
import time
import copy

## defines

cpy = copy.deepcopy

## WebBot class

class WebBot(BotBase):

    """ webbot just inherits from botbase for now. """

    def __init__(self, cfg=None, users=None, plugs=None, botname="gae-web", *args, **kwargs):
        BotBase.__init__(self, cfg, users, plugs, botname, *args, **kwargs)
        assert self.cfg
        self.isgae = True
        self.type = u"web"

    def _raw(self, txt, target, how, response, end=u"\n"):
        """  put txt to the client. """ 
        if not txt: return
        output = LazyDict()
        output.txt = txt
        output.target = target
        output.how = how
        response.out.write(json.dumps(output) + "\n\n")
        logging.debug("%s - out - %s" % (self.cfg.name, str(output)))

    def outnocb(self, channel, txt, how=None, event=None, origin=None, response=None, dotime=False, *args, **kwargs):
        txt = self.normalize(txt)
        if event and event.how != "background":
            logging.info("%s - out - %s" % (self.cfg.name, txt))
        if "http://" in txt or "https://" in txt:
             for item in re_url_match.findall(txt):
                 logging.debug("web - raw - found url - %s" % item)
                 url = u'<a href="%s" onclick="window.open(\'%s\'); return false;">%s</a>' % (item, item, item)
                 try: txt = txt.replace(item, url)
                 except ValueError:  logging.error("web - invalid url - %s" % url)
        if response: self._raw(txt, event.target, event.how, response)
        else:
            if event:
                e = cpy(event)
                e.txt = txt   
                e.channel = channel
                e.how = event.how or how
            else:
                e = EventBase()
                e.nick = self.cfg.nick
                e.userhost = self.cfg.nick + "@" + "bot"
                e.channel = channel
                e.txt = txt
                e.div = "content_div"
                e.origin = origin
                e.how = how or "overwrite"
                e.headlines = True
            e.update(kwargs)
            self.update_web(e)
        #self.benice(event)

    def normalize(self, txt):
        txt = stripcolor(txt)
        txt = txt.replace("\n", "<br>");
        txt = txt.replace("<", "&lt;")
        txt = txt.replace(">", "&gt;")
        txt = strippedtxt(txt)
        txt = txt.replace("&lt;br&gt;", "<br>")
        txt = txt.replace("&lt;b&gt;", "<b>")
        txt = txt.replace("&lt;/b&gt;", "</b>")
        txt = txt.replace("&lt;i&gt;", "<i>")
        txt = txt.replace("&lt;/i&gt;", "</i>")
        txt = txt.replace("&lt;h2&gt;", "<h2>")
        txt = txt.replace("&lt;/h2&gt;", "</h2>")
        txt = txt.replace("&lt;h3&gt;", "<h3>")
        txt = txt.replace("&lt;/h3&gt;", "</h3>")
        txt = txt.replace("&lt;li&gt;", "<li>")
        txt = txt.replace("&lt;/li&gt;", "</li>")
        return txt

    def update_web(self, event):
        from google.appengine.api.channel import channel as gchan
        channel = event.channel
        chan = ChannelBase(channel, botname="gae-web")
        logging.warn("%s - webchannels are %s" % (self.cfg.name, chan.data.webchannels))
        remove = []
        logging.warn(event.dostring())
        out = Container(event.userhost, event.tojson(), how="gae-web").tojson()
        for c in chan.data.webchannels:
            try:
                if c:
                    logging.warn("%s - sending to channel %s - %s" % (self.cfg.name, c, out))
                    gchan.send_message(c, out)
            except gchan.InvalidChannelClientIdError:
                remove.append(c)
        if remove:
            for c in remove: chan.data.webchannels.remove(c) ; logging.warn("%s - closing channel %s" % (self.cfg.name, c))
            chan.save()

 