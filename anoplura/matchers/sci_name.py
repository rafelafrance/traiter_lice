"""Get scientific names."""


NAMES = {'anoplura', 'mammalia'}


def sci_name(span):
    """Enrich the match."""
    data = {'sci_name': span.text, 'group': span[0].ent_type_}
    return data


SCI_NAME = {
    'name': 'sci_name',
    'traits': [
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
