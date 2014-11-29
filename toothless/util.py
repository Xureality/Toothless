import re

from jsonobject.base_properties import AssertTypeProperty


NORMALISED_REPRESENTATION_STRIPPED_CHARS = re.compile('\W+')


class AsciiStringProperty(AssertTypeProperty):
    _type = (unicode, str)

    def selective_coerce(self, obj):
        if isinstance(obj, unicode):
            obj = str(obj)
        return obj


def dispatch(chain, *args, **kwargs):
    for handler in chain:
        if handler(*args, **kwargs):
            break


def humanise_list(items):
    if not items:
        return 'nothing'
    elif len(items) == 1:
        return 'just ' + items[0]
    elif len(items) == 2:
        return ' and '.join(items)
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]


def normalise(string):
    return NORMALISED_REPRESENTATION_STRIPPED_CHARS.sub('', string).lower()
