from collections import defaultdict
import logging
import inspect

# Default value of the dictionary will be list
subscribers = defaultdict(list)

def subscribe(event_type, fn):
    logging.debug("New event type subscribed : " + str(event_type))
    subscribers[event_type].append(fn)

def post_event(event_type, data=None):
    logging.debug(f"Event {str(event_type)} posted from {inspect.stack()[1][3]}!")

    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)