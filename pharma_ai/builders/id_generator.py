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
        "ATC": IDGenerator("ATC"),
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