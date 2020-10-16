"""Get scientific names."""

from ..pylib.util import REPLACE, TRAIT_STEP

NAMES = {'src', 'mammalia'}


def sci_name(span):
    """Enrich the match."""
    data = {
        'sci_name': REPLACE.get(span.lower_, span.lower_),
        'group': span[0].ent_type_}
    return data


SCI_NAME = {
    TRAIT_STEP: [
        {
            'label': 'sci_name',
            'on_match': sci_name,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': list(NAMES)}},
                ],
            ],
        },
    ],
}