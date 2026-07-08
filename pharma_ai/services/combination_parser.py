import re
import logging
from pharma_ai.services.normalization import NormalizationEngine
# Logger Setup
logger = logging.getLogger(__name__)

class CombinationParser:
    def __init__(self):
        self.norm = NormalizationEngine()
        self.sep_pattern = r'\+|\&|\/|\bwith\b|\band\b'

    def parse(self, name):
        """Structured Component Resolution સાથેનું મજબૂત Parser."""
        try:
            raw_parts = re.split(self.sep_pattern, name, flags=re.IGNORECASE)
            components = []
            
            for part in raw_parts:
                part = part.strip()
                if not part:  # Empty components skipped
                    continue
                
                # NormalizationEngine નો ઉપયોગ (Single Source of Truth)
                try:
                    norm_result = self.norm.normalize(part)
                    components.append({
                        "name": norm_result["normalized_name"],
                        "strength": norm_result["metadata"]["strength"],
                        "unit": norm_result["metadata"]["unit"],
                        "dosage_form": norm_result["metadata"]["dosage_form"]
                    })
                except Exception as e:
                    logger.error(f"Failed to normalize component '{part}': {e}")
                    continue
            
            return {
                "is_combination": len(components) > 1,
                "components": components,
                "error": None if components else "Parsing Failed"
            }
            
        except Exception as e:
            logger.exception(f"Critical error in CombinationParser: {e}")
            return {"is_combination": False, "components": [], "error": str(e)}