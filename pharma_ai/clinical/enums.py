from enum import Enum, auto

class MatchType(Enum):
    EXACT_GENERIC = auto()
    EXACT_BRAND = auto()
    ALIAS = auto()
    PARTIAL = auto()
    FUZZY = auto()
    COMBINATION = auto()