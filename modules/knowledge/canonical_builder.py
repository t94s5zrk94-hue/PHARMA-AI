"""
Canonical Generic Builder.
Refactored for Production Governance & Knowledge Integrity.
"""

import re
import json
import csv
from pathlib import Path
from typing import Tuple, List
from modules.clinical import ClinicalNormalizer
from .models import CanonicalDrug

class CanonicalGenericBuilder:
    def __init__(self, dosage_forms_path: str, separator_patterns_path: str):
        self.dosage_dict = self._load_json(dosage_forms_path)
        self.separators = self._load_json(separator_patterns_path).get("separators", [])
        
        # 1. Config Validation (Startup Governance)
        self._validate_config()
        
        # 2. Precompute Regex & Lookups
        self.strength_pattern = re.compile(r"(\d+\.?\d*\s*(?:mg|g|mcg|ml|iu|%))", re.IGNORECASE)
        self.split_pattern = re.compile(f"({'|'.join(map(re.escape, self.separators))})", re.IGNORECASE)
        self.alias_lookup = self._build_alias_lookup()

    def _load_json(self, path: str):
        with open(path, 'r') as f: return json.load(f)

    def _validate_config(self):
        """Governance check: Ensure unique aliases and valid structure."""
        seen_aliases = set()
        for key, data in self.dosage_dict.items():
            for alias in data.get("aliases", []):
                if alias.lower() in seen_aliases:
                    raise ValueError(f"Duplicate alias found in config: {alias}")
                seen_aliases.add(alias.lower())

    def _build_alias_lookup(self):
        lookup = {}
        all_aliases = []
        for key, data in self.dosage_dict.items():
            for alias in data.get("aliases", []):
                all_aliases.append((alias.lower(), key))
        return {a: k for a, k in sorted(all_aliases, key=lambda x: len(x[0]), reverse=True)}

    def _log_unknown_form(self, text: str):
        """Audit logging for unknown dosage forms."""
        report_path = Path("reports/knowledge/unknown_dosage_forms.csv")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([text])

    def build(self, product_name: str) -> CanonicalDrug:
        source_text = product_name
        normalized_name = ClinicalNormalizer.normalize(product_name)
        
        dosage_form, clean_text = self._detect_dosage_form(normalized_name)
        
        # Governance: Unknown dosage form handling
        if dosage_form == "unknown":
            self._log_unknown_form(source_text)
            
        strengths = self.strength_pattern.findall(clean_text)
        text_no_strength = self.strength_pattern.sub("", clean_text)
        ingredients = [p.strip() for p in self.split_pattern.split(text_no_strength) 
                       if p.strip() and not self.split_pattern.match(p)]
        
        form_meta = self.dosage_dict.get(dosage_form, {})
        
        return CanonicalDrug(
            source_text=source_text,
            normalized_name=normalized_name.strip(),
            ingredients=tuple(ingredients),
            strengths=tuple(strengths),
            dosage_form=dosage_form,
            route=form_meta.get("route", "UNKNOWN"),
            category=form_meta.get("category", "UNKNOWN"),
            is_combination=len(ingredients) > 1
        )

    def _detect_dosage_form(self, text: str) -> Tuple[str, str]:
        for alias, canonical in self.alias_lookup.items():
            if re.search(rf"\b{re.escape(alias)}\b", text):
                return canonical, re.sub(rf"\b{re.escape(alias)}\b", "", text, flags=re.IGNORECASE).strip()
        return "unknown", text