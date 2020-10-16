"""Base matcher object."""

from traiter.spacy_nlp.matcher import SpacyMatcher

from .body_part import BODY_PART
# from .elevation import ELEVATION
# from .event_date import COLLECTION_DATE
from .length import LENGTH
# from .max_width import MAX_WIDTH
from .numeric import NUMERIC
# from .sci_name import SCI_NAME
# from .setae_count import SETAE_COUNT
# from .sex_count import SEX_COUNT
from .size import SIZE
from ..pylib.util import ATTACH_STEP, GROUP_STEP, NUMERIC_STEP, TERMS, \
    TRAIT_STEP

MATCHERS = [BODY_PART, LENGTH, NUMERIC, SIZE]


class Matcher(SpacyMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
        self.add_patterns(MATCHERS, NUMERIC_STEP)
        self.add_patterns(MATCHERS, GROUP_STEP)
        self.add_patterns(MATCHERS, TRAIT_STEP)
        self.add_patterns(MATCHERS, ATTACH_STEP)