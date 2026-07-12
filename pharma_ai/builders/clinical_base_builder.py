"""
Clinical Base Builder

Reusable base class for all Clinical Builders.

Phase 16.1 – Clinical Framework Refactoring
"""

from __future__ import annotations

import time

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import IDGenerator

class ClinicalBaseBuilder(BaseBuilder, ABC):
    """
    Base class for all Clinical Builders.

    Provides the common production pipeline used by:

    - Interaction
    - Contraindication
    - Warning
    - Side Effect
    - Pregnancy
    - Lactation
    - Renal
    - Hepatic
    - Monitoring
    - Evidence
    """

    # ---------------------------------------------------------
    # Child Builder Configuration
    # ---------------------------------------------------------

    INPUT_FILE: Path | str | None = None
    OUTPUT_FILE: Path | str | None = None

    REQUIRED_COLUMNS: list[str] = []
    OUTPUT_COLUMNS: list[str] = []

    ID_PREFIX: str = ""
    MASTER_KEY: str = ""
    # Duplicate & Merge Configuration
    DUPLICATE_COLUMNS: list[str] = []
    MERGE_COLUMNS: list[str] = []

    # Metadata Configuration
    VERSION: str = "1.0"
    SOURCE: str = "Pharma AI"
    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self):

        if self.INPUT_FILE is None:
            raise ValueError("INPUT_FILE is not configured.")

        if self.OUTPUT_FILE is None:
            raise ValueError("OUTPUT_FILE is not configured.")
        
        if not self.REQUIRED_COLUMNS:
            raise ValueError(
                "REQUIRED_COLUMNS is not configured."
            )

        if not self.OUTPUT_COLUMNS:
            raise ValueError(
                "OUTPUT_COLUMNS is not configured."
            )

        if not self.ID_PREFIX:
            raise ValueError(
                "ID_PREFIX is not configured."
            )

        if not self.MASTER_KEY:
            raise ValueError(
                "MASTER_KEY is not configured."
            )

        if not self.MERGE_COLUMNS:
            raise ValueError(
                "MERGE_COLUMNS is not configured."
            )

        super().__init__(
            input_file=str(self.INPUT_FILE),
            output_path=str(self.OUTPUT_FILE),
            required_columns=self.REQUIRED_COLUMNS,
        )

        self.master_df = pd.DataFrame()

        self.logger.info(
            "%s initialized.",
            self.__class__.__name__,
        )

    # ---------------------------------------------------------
    # Optional Hook Methods
    # ---------------------------------------------------------

    def pre_process(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Optional preprocessing.

        Child builders may override.
        """
        return df

    def post_process(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Optional postprocessing.

        Child builders may override.
        """
        return df

    # ---------------------------------------------------------
    # Required Business Validation
    # ---------------------------------------------------------

    @abstractmethod
    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate module-specific business rules.
        """
        pass

    # ---------------------------------------------------------
    # Load Existing Master
    # ---------------------------------------------------------

    def _load_existing_master(self) -> pd.DataFrame:
        """
        Load the existing master CSV.

        Returns
        -------
        pd.DataFrame
            Existing master dataframe.
        """

        self.logger.info("Loading existing master...")

        if self.output_path.exists():

            master_df = pd.read_csv(
                self.output_path,
                dtype=str,
            )

            self.logger.info(
                "Loaded %d existing records.",
                len(master_df),
            )

            return master_df

        self.logger.info(
            "No existing master found. Creating empty master."
        )

        self.master_df = pd.DataFrame(
            columns=self.OUTPUT_COLUMNS,
            )

        return self.master_df


    # ---------------------------------------------------------
    # Duplicate Validation
    # ---------------------------------------------------------

    def _validate_duplicates(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate duplicate records.
        """

        if not self.DUPLICATE_COLUMNS:
            return df

        self.logger.info(
            "Checking duplicate records..."
        )

        duplicate_mask = df.duplicated(
            subset=self.DUPLICATE_COLUMNS,
            keep=False,
        )

        if duplicate_mask.any():

            duplicates = df.loc[
                duplicate_mask,
                self.DUPLICATE_COLUMNS,
            ]

            raise ValueError(
                f"Duplicate records found:\n{duplicates}"
            )

        self.logger.info(
            "Duplicate validation passed."
        )

        return df


    # ---------------------------------------------------------
    # Assign IDs
    # ---------------------------------------------------------

    def _assign_ids(
        self,
        existing_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Preserve existing IDs and assign IDs only to
        newly discovered records.
        """

        self.logger.info("Assigning IDs...")

        generator = IDGenerator(
            prefix=self.ID_PREFIX,
        )

        # First build

        if existing_df.empty:

            new_df[self.MASTER_KEY] = generator.generate(
                last_id=None,
                count=len(new_df),
            )

            return new_df

        existing_keys = existing_df[
            self.MERGE_COLUMNS + [self.MASTER_KEY]
        ]

        merged = new_df.merge(
            existing_keys,
            on=self.MERGE_COLUMNS,
            how="left",
        )

        new_mask = merged[self.MASTER_KEY].isna()

        if not new_mask.any():

            self.logger.info(
                "No new records found."
            )

            return merged

        last_id = (
            existing_df[self.MASTER_KEY]
            .dropna()
            .iloc[-1]
        )

        new_ids = generator.generate(
            last_id=last_id,
            count=int(new_mask.sum()),
        )

        merged.loc[
            new_mask,
            self.MASTER_KEY,
        ] = new_ids

        self.logger.info(
            "Existing=%d | New=%d",
            (~new_mask).sum(),
            new_mask.sum(),
        )

        return merged
    
    # ---------------------------------------------------------
    # Add Metadata
    # ---------------------------------------------------------

    def _add_metadata(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add standard metadata columns.
        """

        self.logger.info("Adding metadata...")

        df = df.copy()

        timestamp = pd.Timestamp.now()

        # Preserve existing created_at during updates
        if "created_at" not in df.columns:
            df["created_at"] = timestamp
        else:
            df["created_at"] = df["created_at"].fillna(timestamp)

        df["updated_at"] = timestamp

        if "source" not in df.columns:
            df["source"] = self.SOURCE
        else:
            df["source"] = df["source"].fillna(self.SOURCE)

        if "version" not in df.columns:
            df["version"] = self.VERSION
        else:
            df["version"] = df["version"].fillna(self.VERSION)

        self.logger.info("Metadata added.")

        return df


    # ---------------------------------------------------------
    # Merge Master
    # ---------------------------------------------------------

    def _merge_master(
        self,
        existing_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge new records into the existing master.

        Existing IDs are preserved.
        Latest record overwrites previous record.
        """

        self.logger.info("Merging master...")

        # First build
        if existing_df.empty:

            self.logger.info(
                "First build detected."
            )

            return new_df

        final_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True,
        )

        final_df = final_df.drop_duplicates(
            subset=self.MERGE_COLUMNS,
            keep="last",
        )

        # Keep output column order
        if self.OUTPUT_COLUMNS:
            final_df = final_df[self.OUTPUT_COLUMNS]

        self.logger.info(
            "Existing=%d | New=%d | Final=%d",
            len(existing_df),
            len(new_df),
            len(final_df),
        )

        return final_df 
    
    # ---------------------------------------------------------
    # Build Pipeline
    # ---------------------------------------------------------

    def build(self) -> dict:
        """
        Execute the complete clinical builder pipeline.
        """

        start_time = time.time()

        self.logger.info(
            "Starting %s...",
            self.__class__.__name__,
        )

        # -------------------------------------------------
        # Step 1 : Validate Input
        # -------------------------------------------------

        self.validate_input()

        # -------------------------------------------------
        # Step 2 : Load CSV
        # -------------------------------------------------

        new_df = self.load_csv()

        input_count = len(new_df)

        # -------------------------------------------------
        # Step 3 : Validate Schema
        # -------------------------------------------------

        self.validate_columns(new_df)

        # -------------------------------------------------
        # Step 4 : Optional Pre-processing
        # -------------------------------------------------

        new_df = self.pre_process(new_df)

        # -------------------------------------------------
        # Step 5 : Business Rules
        # -------------------------------------------------

        new_df = self._validate_business_rules(new_df)

        # -------------------------------------------------
        # Step 6 : Optional Post-processing
        # -------------------------------------------------

        new_df = self.post_process(new_df)

        # -------------------------------------------------
        # Step 7 : Duplicate Validation
        # -------------------------------------------------

        new_df = self._validate_duplicates(new_df)

        # -------------------------------------------------
        # Step 8 : Load Existing Master
        # -------------------------------------------------

        existing_df = self._load_existing_master()

        # -------------------------------------------------
        # Step 9 : Assign IDs
        # -------------------------------------------------

        new_df = self._assign_ids(
            existing_df,
            new_df,
        )

        # -------------------------------------------------
        # Step 10 : Metadata
        # -------------------------------------------------

        new_df = self._add_metadata(new_df)

        # -------------------------------------------------
        # Step 11 : Merge Master
        # -------------------------------------------------

        final_df = self._merge_master(
            existing_df,
            new_df,
        )

        # -------------------------------------------------
        # Step 12 : Output Columns
        # -------------------------------------------------

        if self.OUTPUT_COLUMNS:
            final_df = final_df[self.OUTPUT_COLUMNS]

        # -------------------------------------------------
        # Step 13 : Save
        # -------------------------------------------------

        self.save_csv(final_df)

        self.logger.info(
            "%s completed successfully.",
            self.__class__.__name__,
        )

        return self.get_summary(
            start_time=start_time,
            input_count=input_count,
            output_count=len(final_df),
            dups_removed=0,
            skipped=0,
            failed=0,
            status="SUCCESS",
        )