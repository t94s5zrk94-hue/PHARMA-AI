import re
from typing import List, Optional

class IDGenerator:
    """
    Pharma AI Builder Framework માટે સેન્ટ્રલ ID જનરેટર.
    """

    def __init__(self, prefix: str, padding: int = 6):
        self.prefix = prefix.upper()  # સુધારો 3: Prefix હંમેશા Uppercase માં
        self.padding = padding
        # પેટર્ન: Prefix + Numbers
        self.pattern = re.compile(rf"^{self.prefix}(\d+)$")

    def _get_number(self, last_id: Optional[str]) -> int:
        # સુધારો 2: Empty string, whitespace, કે None ને handle કરે છે
        if not last_id or not last_id.strip():
            return 0
            
        match = self.pattern.match(last_id.strip())
        if not match:
            raise ValueError(f"Invalid ID format: {last_id}. Expected prefix: {self.prefix}")
        return int(match.group(1))

    def generate_next(self, last_id: Optional[str] = None, count: int = 1) -> List[str]:
        """
        છેલ્લા ID પરથી આગામી N IDs જનરેટ કરે છે.
        """
        # સુધારો 1: Count Validation
        if count < 1:
            raise ValueError("count must be greater than zero")
            
        start_num = self._get_number(last_id)
        new_ids = []
        
        for i in range(1, count + 1):
            next_num = start_num + i
            new_id = f"{self.prefix}{next_num:0{self.padding}d}"
            new_ids.append(new_id)
            
        return new_ids

# --- Wrapper API (સુધારો 4: બધા જ જરૂરી Wrappers) ---

def get_next_generic_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("GEN").generate_next(last_id, count)

def get_next_company_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("CMP").generate_next(last_id, count)

def get_next_brand_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("BRD").generate_next(last_id, count)

def get_next_product_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("PRD").generate_next(last_id, count)

def get_next_atc_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("ATC").generate_next(last_id, count)

def get_next_therapeutic_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("THR").generate_next(last_id, count)

def get_next_pharmacological_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("PHR").generate_next(last_id, count)

def get_next_mapping_id(last_id: Optional[str], count: int = 1) -> List[str]:
    return IDGenerator("MAP").generate_next(last_id, count)