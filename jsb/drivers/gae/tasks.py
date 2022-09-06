# jsb/gae/tasks.py
#
#

""" appengine tasks related classes and functions. """

## jsb imports

from jsb.utils.exception import handle_exception

## google imports

from google.appengine.api.labs.taskqueue import Task, Queue

## simplejson imports

from jsb.imports import getjson
json = getjson()

## basic imports

import uuid

## Event Classes

class BotEvent(Task):
    pass

## defines

queues = []
for i in range(9):
    queues.append(Queue("queue" + str(i)))

## start_botevent function

counter = 0

def start_botevent(bot, event, speed=None):
    """ start a new botevent task. """
    try:
        global counter
        counter += 1
        try: speed = int(speed)
        except: speed = "backend"
        event.botevent = True
        e = event.usercmnd or event.txt.split()[0]
        name = e + "-" + str(uuid.uuid4())
        payload = json.dumps({ 'bot': bot.tojson(),
                          'event': event.tojson()
                        })
        be = BotEvent(name=name, payload=payload, url="/tasks/botevent")
        if speed == "backend": Queue("backend").add(be)
        else:
            try: queues[speed or event.speed].add(be)
            except TypeError: queues[speed or event.speed].add(be)
    except Exception, ex: 
        handle_exception()
