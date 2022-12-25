# -----------------* Code-Based From *-----------------
# https://dev.to/kuba_szw/build-your-own-event-system-in-python-5hk6
# -----------------------------------------------

from collections import defaultdict

subscribers = defaultdict(list)

def subscribe(event_name, fn):
    subscribers[event_name].append(fn)

def unsubscribe(event_name, fn):
    subscribers[event_name].remove(fn)

def post_event(event_name, data):
    if event_name in subscribers:
        for fn in subscribers[event_name]:
            fn(data)
