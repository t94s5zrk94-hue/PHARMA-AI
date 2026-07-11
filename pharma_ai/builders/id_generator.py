import re
import logging
from typing import Optional, List

# Setup simple logging
logger = logging.getLogger(__name__)

class IDGenerator:
    """Core utility for ID generation with robust regex validation."""
    def __init__(self, prefix: str, padding: int = 6):
        self.prefix = prefix.upper()
        self.padding = padding
        # Regex to ensure ID starts exactly with the prefix followed by digits
        self.pattern = re.compile(rf"^{self.prefix}(\d+)$")

    def generate(self, last_id: Optional[str], count: int = 1) -> List[str]:
        if count < 1:
            raise ValueError("count must be greater than zero")
        
        start_num = 0
        if last_id and last_id.strip():
            match = self.pattern.fullmatch(last_id.strip())
            if match:
                start_num = int(match.group(1))
            else:
                logger.warning(f"Corrupted or invalid ID encountered: '{last_id}'. Defaulting start_num to 0.")
                start_num = 0
        
        return [f"{self.prefix}{(start_num + i):0{self.padding}d}" for i in range(1, count + 1)]

# Global instances
_MANAGERS = {
    "GEN": IDGenerator("GEN"),
    "CMP": IDGenerator("CMP"),
    "BRD": IDGenerator("BRD"),
    "PRD": IDGenerator("PRD"),
    "ATC": IDGenerator("ATC"),
    "THR": IDGenerator("THR"),
    "PHR": IDGenerator("PHR"),
    "MAP": IDGenerator("MAP"),

    # ===== Clinical =====
    "INT": IDGenerator("INT"),
    "CON": IDGenerator("CON"),
    "WRN": IDGenerator("WRN"),
    "SEF": IDGenerator("SEF"),
    "PRG": IDGenerator("PRG"),
    "LAC": IDGenerator("LAC"),
    "REN": IDGenerator("REN"),
    "HEP": IDGenerator("HEP"),
    "MON": IDGenerator("MON"),
    "EVD": IDGenerator("EVD"),
}

# --- Backward Compatible APIs ---

def get_next_generic_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["GEN"].generate(last_id, count)

def get_next_company_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["CMP"].generate(last_id, count)

def get_next_brand_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["BRD"].generate(last_id, count)

def get_next_atc_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["ATC"].generate(last_id, count)
def get_next_mapping_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["MAP"].generate(last_id, count)
def get_next_therapeutic_id(
    last_id: Optional[str],
    count: int = 1,
) -> List[str]:
    """
    Generate sequential Therapeutic Class IDs.

    Example:
        THR000001
        THR000002
    """
    return _MANAGERS["THR"].generate(last_id, count)

def get_next_pharmacological_id(
    last_id: Optional[str],
    count: int = 1,
) -> List[str]:
    """
    Generate sequential Pharmacological Class IDs.

    Example:
        PHR000001
        PHR000002
    """
    return _MANAGERS["PHR"].generate(last_id, count)
def get_next_interaction_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["INT"].generate(last_id, count)


def get_next_contraindication_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["CON"].generate(last_id, count)


def get_next_warning_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["WRN"].generate(last_id, count)


def get_next_side_effect_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["SEF"].generate(last_id, count)


def get_next_pregnancy_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["PRG"].generate(last_id, count)


def get_next_lactation_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["LAC"].generate(last_id, count)


def get_next_renal_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["REN"].generate(last_id, count)


def get_next_hepatic_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["HEP"].generate(last_id, count)


def get_next_monitoring_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["MON"].generate(last_id, count)


def get_next_evidence_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return _MANAGERS["EVD"].generate(last_id, count)