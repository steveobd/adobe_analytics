from __future__ import absolute_import

import copy
import datetime
import six
from dateutil.parser import parse as parse_date


def date(obj):
    # used to ensure compatibility with Python3 without having to use six
    try:
        basestring
    except NameError:
        basestring = str

    if obj is None:
        return None
    elif isinstance(obj, datetime.date):
        if hasattr(obj, 'date'):
            return obj.date()
        else:
            return obj
    elif isinstance(obj, six.string_types):
        return parse_date(obj).date()
    elif isinstance(obj, six.text_type):
        return parse_date(str(obj)).date()
    else:
        raise ValueError("Can only convert strings into dates, received {}"
                         .format(obj.__class__))


def wrap(obj):
    if isinstance(obj, list):
        return obj
    else:
        return [obj]


def translate(d, mapping):
    d = copy.copy(d)

    for src, dest in mapping.items():
        if src in d:
            d[dest] = d[src]
            del d[src]
    return d
