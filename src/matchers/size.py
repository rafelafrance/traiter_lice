"""Parse size notations."""

import re

from traiter.pylib.util import to_positive_float, to_positive_int

from .shared import CLOSE, COMMA, EQ, INT, NUMBER, OPEN


def size(span):
    """Enrich a phrase match."""
    data = {}

    for token in span:
        if token.ent_type_ in ('range', 'mean', 'n'):
            data = {**token._.data, **data}
        else:
            return {}

    return data


def sample(span):
    """Convert the span into a single integer."""
    if values := [t.text for t in span if re.match(INT, t.text)]:
        if (value := to_positive_int(values[0])) is not None:
            return dict(n=value)
    return {}


def mean(span):
    """Convert the span into a single float."""
    if values := [t.text for t in span if re.match(NUMBER, t.text)]:
        if (value := to_positive_float(values[0])) is not None:
            data = dict(mean=value)
            if units := [t.text for t in span if t.ent_type_ == 'units']:
                data['mean_units'] = units[0]
            return data
    return {}


BAR = ['bar', 'bars']

SIZE = {
    'name': 'size',
    'groupers': [
        {
            'label': 'bar',
            'patterns': [[
                {'LOWER': {'IN': BAR}},
                {'TEXT': {'IN': COMMA}, 'OP': '?'},
            ]],
        },
        {
            'label': 'mean',
            'on_match': mean,
            'patterns': [[
                {'TEXT': {'IN': COMMA}, 'OP': '?'},
                {'LOWER': 'mean'},
                {'TEXT': {'REGEX': NUMBER}},
                {'ENT_TYPE': 'units'},
            ]],
        },
        {
            'label': 'n',
            'on_match': sample,
            'patterns': [[
                {'TEXT': {'IN': OPEN}, 'OP': '?'},
                {'LOWER': 'n'},
                {'TEXT': {'IN': EQ}},
                {'TEXT': {'REGEX': INT}},
                {'TEXT': {'IN': CLOSE}, 'OP': '?'},
            ]],
        },
    ],
    'traits': [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'ENT_TYPE': 'bar', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'mean', 'OP': '?'},
                    {'ENT_TYPE': 'n', 'OP': '?'},
                ],
            ],
        },
    ],
}
