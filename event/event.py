from collections import defaultdict
import logging

# Default value of the dictionary will be list
subscribers = defaultdict(list)

def subscribe(event_type, fn):
    logging.debug("New event type subscribed : " + str(event_type))
    subscribers[event_type].append(fn)

def post_event(event_type, data=None):
    logging.debug("Event " + str(event_type) + " posted !")

    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)