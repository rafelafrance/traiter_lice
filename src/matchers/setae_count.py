"""Extract setae count notations."""

from ..pylib.util import CLOSE, OPEN, REPLACE, TRAIT_STEP


def setae_count(span):
    """Enrich the match."""
    data = {}
    location = []
    for token in span:
        label = token.ent_type_
        if label == 'seta':
            data['setae'] = token.lower_
        elif label == 'seta_abbrev':
            data['setae'] = 'setae'
            data['type'] = REPLACE.get(token.lower_, token.lower_)
        elif label in ('location', 'part'):
            location.append(token.lower_)
        elif label == 'integer':
            data = {**data, **token._.data}
        elif label == 'group':
            data['group'] = token.lower_
    if data.get('count', data.get('low')) is None:
        data['present'] = True
    if location:
        data['type'] = ' '.join(location)
    return data


def multiple_setae_count(span):
    """Handle multiple setae in one match."""
    data = {}
    low, high = 0, 0
    for token in span:
        label = token.ent_type_
        if label == 'seta':
            data['setae'] = token.lower_
        elif label == 'seta_abbrev':
            data['setae'] = 'setae'
            data['type'] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'integer':
            if token._.data.get('count'):
                low += token._.data['count']
            else:
                low += token._.data.get('low', 0)
                high += token._.data.get('high', 0)
        elif label == 'group':
            data['group'] = token.lower_

    if high and low:
        data['low'] = low
        data['high'] = high
    else:
        data['count'] = low

    return data


SETAE_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'setae_count',
            'on_match': setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                    {'POS': {'IN': ['ADP', 'ADJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'group'}
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                ],
                [
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                    {'POS': {'IN': ['ADP', 'ADJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'group'}
                ],
                [
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': 'seta'},
                ],
            ],
        },
        {
            'label': 'setae_count',
            'on_match': multiple_setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': {'IN': ['location']}, 'OP': '*'},
                    {'ENT_TYPE': {'IN': ['location', 'body_part']}, 'OP': '?'},
                    {'ENT_TYPE': 'seta'},
                ],
            ],
        },
    ],
}