import re
import json
import logging

class NormalizationEngine:
    def __init__(self, rules_path='config/rules.json', syn_path='config/synonyms.json'):
        self.logger = logging.getLogger(__name__)
        self.rules = self._load_json(rules_path)
        self.synonyms = self._load_json(syn_path)

    def _load_json(self, path):
        try:
            with open(path, 'r') as f: return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {path}: {e}")
            return {}

    def normalize(self, name):
        original = name
        history = ["Original"]
        warnings = []
        score = 1.0
        
        # 1. Cleaning & Case
        name = str(name).lower().replace('®', '').replace('™', '')
        history.append("Case Normalized & Unicode Cleaned")
        
        # 2. Extract Metadata
        meta = {
            "strength": None, "unit": None, "dosage_form": None, 
            "release_form": None, "pharmacopoeia": None
        }
        
        # Strength Extraction
        match = re.search(r'(\d+\.?\d*)\s*(mg|g|ml|%|w/w|iu|mcg|units)', name)
        if match:
            meta["strength"], meta["unit"] = match.groups()
            name = re.sub(r'\d+\.?\d*\s*(mg|g|ml|%|w/w|iu|mcg|units)', '', name)
            history.append("Strength Extracted")
        else:
            score -= 0.1 # Penalty for missing strength in potent drugs

        # Pharmacopoeia & Forms
        meta["pharmacopoeia"] = self._extract_match(name, self.rules.get('pharmacopoeia', []))
        meta["dosage_form"] = self._extract_match(name, self.rules.get('dosage_forms', []))
        meta["release_form"] = self._extract_match(name, self.rules.get('release_forms', []))
        
        # 3. Cleanup & Unknown Tokens
        parts = [p for p in name.split() if p not in self.rules.get('pharmacopoeia', []) + self.rules.get('dosage_forms', []) + self.rules.get('release_forms', [])]
        cleaned = re.sub(r'(\+|\&|\/|with|and)', ' + ', " ".join(parts))
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # 4. Synonym & Final Resolve
        final_name = self.synonyms.get(cleaned, cleaned).title()
        
        return {
            "normalized_name": final_name,
            "metadata": meta,
            "confidence": round(max(0.1, score), 2),
            "history": history,
            "warnings": warnings if warnings else None
        }

    def _extract_match(self, name, candidates):
        for c in candidates:
            if re.search(rf'\b{c}\b', name, re.IGNORECASE): return c.upper() if c in self.rules.get('pharmacopoeia', []) else c.title()
        return None