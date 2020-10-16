"""Parse size notations."""

from ..pylib.util import EQ, GROUP_STEP, TRAIT_STEP


def size(span):
    """Enrich a phrase match."""
    data = {}

    for token in span:
        if token.ent_type_ in ('measurement', 'mean', 'n'):
            data = {**token._.data, **data}
    return data


def sample(span):
    """Convert the span into a single integer."""
    values = [t._.data for t in span if t.ent_type_ == 'integer']
    return dict(n=values[0].get('count', values[0].get('low')))


def mean(span):
    """Convert the span into a single float."""
    values = [t._.data for t in span if t.ent_type_ == 'measurement']
    return {
        'mean': values[0].get('low'),
        'mean_units': values[0].get('length_units'),
    }


BAR = ['bar', 'bars']

SIZE = {
    GROUP_STEP: [
        {
            'label': 'bar',
            'patterns': [[
                {'LOWER': {'IN': BAR}},
            ]],
        },
        {
            'label': 'mean',
            'on_match': mean,
            'patterns': [[
                {'LOWER': 'mean'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'ENT_TYPE': 'measurement'},
            ]],
        },
        {
            'label': 'n',
            'on_match': sample,
            'patterns': [[
                {'LOWER': 'n'},
                {'TEXT': {'IN': EQ}},
                {'ENT_TYPE': 'integer'},
            ]],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'ENT_TYPE': 'bar', 'OP': '?'},
                    {'IS_PUNCT': True, 'OP': '?'},
                    {'ENT_TYPE': 'measurement'},
                    {'IS_PUNCT': True, 'OP': '?'},
                    {'ENT_TYPE': 'mean', 'OP': '?'},
                    {'IS_PUNCT': True, 'OP': '?'},
                    {'ENT_TYPE': 'n', 'OP': '?'},
                    {'IS_PUNCT': True, 'OP': '?'},
                ],
            ],
        },
    ],
}
