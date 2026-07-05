import pytest
from modules.clinical.normalizer import ClinicalNormalizer

def test_normalize_none_and_empty():
    """Test handling of None, empty strings, and whitespace-only input."""
    assert ClinicalNormalizer.normalize(None) == ""
    assert ClinicalNormalizer.normalize("") == ""
    assert ClinicalNormalizer.normalize("   ") == ""

def test_normalize_lowercase():
    """Test case normalization."""
    assert ClinicalNormalizer.normalize("Paracetamol") == "paracetamol"
    assert ClinicalNormalizer.normalize("PARACETAMOL") == "paracetamol"

def test_normalize_whitespace():
    """Test whitespace cleanup."""
    assert ClinicalNormalizer.normalize(" Paracetamol    Tablets ") == "paracetamol tablets"

def test_normalize_unicode():
    """Test Unicode NFKC normalization."""
    # Amlodipine with full-width characters
    assert ClinicalNormalizer.normalize("Ａｍｌｏｄｉｐｉｎｅ") == "amlodipine"

def test_normalize_ocr_corrections():
    """Test specific clinical OCR corrections."""
    assert ClinicalNormalizer.normalize("Paracetamo1") == "paracetamol"
    assert ClinicalNormalizer.normalize("Amiodipine") == "amlodipine"
    assert ClinicalNormalizer.normalize("Paracetamol |") == "paracetamol l"

def test_normalize_numeric_integrity():
    """Crucial test: Ensure numeric values are not destroyed."""
    assert ClinicalNormalizer.normalize("500 mg") == "500 mg"