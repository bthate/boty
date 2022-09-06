# boty/plugs/version.py
#
#

""" echo boty version. """

## jsb import

from jsb.lib.config import getmainconfig
from jsb.lib.commands import cmnds
from jsb.lib.aliases import setalias

## version command

def handle_boty_version(bot, ievent):
    """ no arguments - show bot's version. """
    from boty.version import getversion
    version = getversion(bot.type.upper())
    cfg = getmainconfig()
    if cfg.dbenable: version += " " + cfg.dbtype.upper()
    try: 
        from mercurial import context, hg, node, repo, ui
        repository = hg.repository(ui.ui(), '.')
        ctx = context.changectx(repository)
        tip = str(ctx.rev())
    except: tip = None
    if tip: version2 = version + " HG " + tip
    else: version2 = version
    ievent.reply(version2)  

cmnds.add("version", handle_boty_version, ["OPER", "USER", "GUEST"])
setalias("v", "version")