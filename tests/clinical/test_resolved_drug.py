import pytest
from modules.clinical.models import ResolvedDrug
from modules.clinical.enums import MatchType

def test_resolved_drug_valid_creation():
    """Test successful creation of a valid ResolvedDrug object."""
    drug = ResolvedDrug(
        generic_ids=("GEN001",),
        canonical_names=("Paracetamol",),
        matched_value="Crocin",
        confidence=98.5,
        match_type=MatchType.EXACT_BRAND,
        is_combination=False,
        strengths=("500mg",),
        aliases=("PCM",)
    )
    assert drug.confidence == 98.5
    assert drug.is_combination is False

def test_resolved_drug_confidence_validation():
    """Test confidence score bounds (0-100)."""
    with pytest.raises(ValueError, match="confidence must be between 0 and 100"):
        ResolvedDrug(
            generic_ids=("GEN001",),
            canonical_names=("Paracetamol",),
            matched_value="PCM",
            confidence=105.0, # Invalid
            match_type=MatchType.EXACT_GENERIC,
            is_combination=False,
            strengths=("500mg",),
            aliases=()
        )

def test_resolved_drug_length_mismatch():
    """Test structural integrity between generic_ids and canonical_names."""
    with pytest.raises(ValueError, match="generic_ids and canonical_names must have equal length"):
        ResolvedDrug(
            generic_ids=("GEN001",),
            canonical_names=("Paracetamol", "Amlodipine"), # Mismatch
            matched_value="Invalid",
            confidence=90.0,
            match_type=MatchType.COMBINATION,
            is_combination=True,
            strengths=("500mg",),
            aliases=()
        )

def test_resolved_drug_combination_validation():
    """Test is_combination validation logic."""
    with pytest.raises(ValueError, match="is_combination=True requires multiple generic_ids"):
        ResolvedDrug(
            generic_ids=("GEN001",), # Only one ID for a combination
            canonical_names=("Paracetamol",),
            matched_value="PCM",
            confidence=95.0,
            match_type=MatchType.COMBINATION,
            is_combination=True,
            strengths=("500mg",),
            aliases=()
        )

def test_resolved_drug_immutability():
    """Test that ResolvedDrug is immutable."""
    drug = ResolvedDrug(
        generic_ids=("GEN001",),
        canonical_names=("Paracetamol",),
        matched_value="Crocin",
        confidence=98.0,
        match_type=MatchType.EXACT_BRAND,
        is_combination=False,
        strengths=("500mg",),
        aliases=()
    )
    with pytest.raises(AttributeError):
        drug.confidence = 50.0 # Should raise error due to frozen=True