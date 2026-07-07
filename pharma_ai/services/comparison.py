"""Brand comparison services for the Pharma AI application."""

from __future__ import annotations

import re
from threading import Lock
from typing import Any, ClassVar

from pharma_ai.services.database import PharmaDatabase


class BrandComparison:
    """Compare complete medicine information for two brands."""

    _database: ClassVar[PharmaDatabase | None] = None
    _database_lock: ClassVar[Lock] = Lock()

    def __init__(self) -> None:
        self._db = self._get_database()

    @classmethod
    def _get_database(cls) -> PharmaDatabase:
        if cls._database is None:
            with cls._database_lock:
                if cls._database is None:
                    cls._database = PharmaDatabase()
        return cls._database

    def compare_brands(self, brand1: str, brand2: str) -> dict[str, Any]:
        """Load two brands and return a structured comparison result."""

        requested_brands = {
            "brand1": self._normalize_brand_name(brand1),
            "brand2": self._normalize_brand_name(brand2),
        }
        medicines = {
            key: self._load_medicine(brand_name)
            for key, brand_name in requested_brands.items()
        }
        missing_brands = [
            requested_brands[key]
            for key, medicine in medicines.items()
            if medicine is None
        ]

        return {
            "success": not missing_brands,
            "requested_brands": requested_brands,
            "medicines": medicines,
            "missing_brands": missing_brands,
            "message": self._build_status_message(missing_brands),
        }

    def get_comparison_table(
        self,
        result: dict[str, Any],
    ) -> list[dict[str, str]]:
        """Convert a successful comparison into display-ready table rows."""

        medicine1 = result["medicines"].get("brand1")
        medicine2 = result["medicines"].get("brand2")
        brand1 = result["requested_brands"]["brand1"]
        brand2 = result["requested_brands"]["brand2"]

        fields = (
            ("Brand Name", "brand", "Brand_Name"),
            ("Generic Name", "generic", "Generic_Name"),
            ("Strength", "brand", "Strength"),
            ("Dosage Form", "brand", "Dosage_Form"),
            ("Company", "company", "Company_Name"),
            ("Country", "company", "Country"),
            ("Pack Size", "product", "Pack_Size"),
            ("Schedule", "product", "Schedule"),
            ("GST", "product", "GST"),
            (
                "Jan Aushadhi Available",
                "brand",
                "Jan_Aushadhi_Available",
            ),
        )

        return [
            {
                "Field": label,
                brand1: self._get_nested_value(medicine1, section, field),
                brand2: self._get_nested_value(medicine2, section, field),
            }
            for label, section, field in fields
        ]

    def is_same_generic(self, result: dict[str, Any]) -> bool:
        """Return whether both loaded brands contain the same generic."""

        medicine1 = result["medicines"].get("brand1")
        medicine2 = result["medicines"].get("brand2")
        generic1 = self._get_nested_value(
            medicine1,
            "generic",
            "Generic_ID",
            default="",
        )
        generic2 = self._get_nested_value(
            medicine2,
            "generic",
            "Generic_ID",
            default="",
        )
        return bool(
            generic1
            and generic2
            and generic1.casefold() == generic2.casefold()
        )

    def generate_summary(self, result: dict[str, Any]) -> str:
        """Generate a safety-oriented summary of the comparison."""

        if not result["success"]:
            return result["message"]

        brand1 = result["requested_brands"]["brand1"]
        brand2 = result["requested_brands"]["brand2"]

        if self.is_same_generic(result):
            generic_name = self._get_nested_value(
                result["medicines"]["brand1"],
                "generic",
                "Generic_Name",
            )
            return (
                f"{brand1} and {brand2} contain the same generic medicine "
                f"({generic_name}). Compare their strength, dosage form, "
                "manufacturer, pack size, and schedule before use."
            )

        return (
            f"{brand1} and {brand2} contain different generic medicines. "
            "They should not be considered interchangeable without guidance "
            "from a qualified healthcare professional."
        )

    def _load_medicine(self, brand_name: str) -> dict[str, Any] | None:
        if not brand_name:
            return None

        try:
            return self._db.get_complete_medicine(brand_name)
        except (KeyError, TypeError, ValueError, re.error):
            return None

    @classmethod
    def _get_nested_value(
        cls,
        medicine: dict[str, Any] | None,
        section: str,
        field: str,
        default: str = "Not available",
    ) -> str:
        if medicine is None:
            return default

        record = medicine.get(section)
        if record is None or not hasattr(record, "get"):
            return default

        return cls._clean_display_value(record.get(field), default)

    @staticmethod
    def _clean_display_value(value: Any, default: str) -> str:
        if value is None:
            return default

        text = str(value).strip()
        if not text or text.casefold() == "nan":
            return default
        return text

    @staticmethod
    def _normalize_brand_name(value: str) -> str:
        if not isinstance(value, str):
            return ""
        return value.strip()

    @staticmethod
    def _build_status_message(missing_brands: list[str]) -> str:
        if not missing_brands:
            return "Both brands were loaded successfully."

        names = [brand_name or "<empty brand>" for brand_name in missing_brands]
        return f"Brand not found: {', '.join(names)}"
