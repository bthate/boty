# jsb/plugs/core/cfg.py
#
#

""" this plugin manages various configuration settings. """

from jsb.lib.commands import cmnds
from jsb.lib.users import getusers
from jsb.lib.config import getmainconfig

allowset = ["timesleep"]

def handle_cfgset(bot, event):
    if len(event.args) != 3: event.missing("<configname> <variable> <value>") ; return
    name, var, value = event.args
    if not var in allowset: event.reply("setting %s is not allowed") ; return
    if name == "main":
        if not getusers().allowed(event.userhost, "OPER"): event.reply("you need to have OPER permissions to edit the mainconfig.") ; return
        mcfg = getmainconfig()
        mcfg[var] = value
        mcfg.save()
        event.done()
    else: event.reply('we current only support editing the "main" config.') ; return

cmnds.add("cfg-set", handle_cfgset, ["OPER", "USER"])

def handle_cfg(bot, event):
    if len(event.args) != 1: event.missing("<configname>") ; return
    name = event.args[0]
    if name == "main":
        if not getusers().allowed(event.userhost, "OPER"): event.reply("you need to have OPER permissions to edit the mainconfig.") ; return
        event.reply(getmainconfig().fordisplay())

cmnds.add("cfg", handle_cfg, ["OPER", "USER"])
