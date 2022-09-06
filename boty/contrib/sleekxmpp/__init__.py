"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys, os
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))

from basexmpp import BaseXMPP
from clientxmpp import ClientXMPP
from componentxmpp import ComponentXMPP
from stanza import Message, Presence, Iq
from xmlstream.handler import *
from xmlstream import XMLStream, RestartStream
from xmlstream.matcher import *
from xmlstream.stanzabase import StanzaBase, ET

from version import __version__, __version_info__
