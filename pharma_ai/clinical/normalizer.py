"""
Clinical Normalizer Module.
Handles text normalization pipeline for OCR, Voice, and Multi-lingual inputs.
"""

import unicodedata
import re
from typing import Optional

class ClinicalNormalizer:
    """
    Pipeline-based normalizer for clinical input.
    """

    @staticmethod
    def normalize(query: Optional[str]) -> str:
        """
        Public API for text normalization pipeline.
        """
        if not query or not str(query).strip():
            return ""

        text = ClinicalNormalizer._unicode_normalize(str(query))
        text = ClinicalNormalizer._case_normalize(text)
        text = ClinicalNormalizer._ocr_cleanup(text)
        text = ClinicalNormalizer._whitespace_normalize(text)

        return text

    @staticmethod
    def _unicode_normalize(text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def _case_normalize(text: str) -> str:
        return text.lower()

    @staticmethod
    def _ocr_cleanup(text: str) -> str:
        """
        Corrects common OCR mistakes using context-aware rules.
        """
        # Rules that are safe and non-destructive to numeric values
        corrections = {
            r"paracetamo1": "paracetamol",
            r"amiodipine": "amlodipine",
            r"\|": "l",
        }
        for pattern, replacement in corrections.items():
            text = re.sub(pattern, replacement, text)
        return text

    @staticmethod
    def _whitespace_normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()