import re

from collections import deque
from cunidecode import unidecode
from jsonobject.base_properties import AssertTypeProperty
from monotonic import monotonic


NORMALISED_REPRESENTATION_STRIPPED_CHARS = re.compile('\W+')


class AsciiStringProperty(AssertTypeProperty):
    _type = (unicode, str)

    def selective_coerce(self, obj):
        if isinstance(obj, unicode):
            obj = str(obj)
        return obj


class RateLimiter:
    def __init__(self, quota, window):
        # preconditions
        assert(quota > 0)
        assert(window > 0)

        # save params
        self.quota = quota
        self.window = window

        # init misc
        self.state = {}

    def intend(self, ident):
        # preconditions
        assert(self.quota > 0)
        assert(self.window > 0)

        # init
        now = monotonic()
        if (ident not in self.state):
            self.state[ident] = (deque(), 0)
        (queue, failed_intents) = self.state[ident]

        # flush expired intents
        while (queue and ((now - queue[0]) > self.window)):
            queue.popleft()

        # work out what to do with current intent
        if (len(queue) < self.quota):
            queue.append(now)
            failed_intents = 0
        else:
            failed_intents += 1

        # postconditions
        assert(len(queue) <= self.quota)

        # save state
        self.state[ident] = (queue, failed_intents)

        # generate bean counters
        quota_left = self.quota - len(queue) - failed_intents
        window_left = self.window - (now - queue[0])
        return (quota_left, window_left)


def dispatch(chain, *args, **kwargs):
    for handler in chain:
        if handler(*args, **kwargs):
            return True
    return False


def humanise_list(items, zero_items='nothing', one_item_prefix='just '):
    if not items:
        return zero_items
    elif len(items) == 1:
        return one_item_prefix + items[0]
    elif len(items) == 2:
        return ' and '.join(items)
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]


def normalise(string):
    transliterated_string = unidecode(string.decode('utf-8'))
    normalised_string = NORMALISED_REPRESENTATION_STRIPPED_CHARS.sub(
        '', transliterated_string
    ).lower()
    return normalised_string
