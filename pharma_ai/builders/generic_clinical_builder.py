"""
Generic Clinical Base Builder

Shared framework for clinical builders that require
Generic_Name -> Generic_ID mapping.

Used by:
    - RenalBuilder
    - HepaticBuilder
    - MonitoringBuilder
    - EvidenceBuilder
"""

import logging
from pathlib import Path

import pandas as pd

from pharma_ai.builders.clinical_base_builder import (
    ClinicalBaseBuilder,
)


class GenericClinicalBuilder(ClinicalBaseBuilder):
    """
    Base class for all Generic-ID based
    Clinical Builders.
    """

    def __init__(
        self,
        input_file,
        output_file,
        required_columns,
        output_columns,
        id_prefix,
        master_key,
        duplicate_columns,
        merge_columns,
    ):

        super().__init__(
            input_file=input_file,
            output_file=output_file,
            required_columns=required_columns,
            output_columns=output_columns,
            id_prefix=id_prefix,
            master_key=master_key,
            duplicate_columns=duplicate_columns,
            merge_columns=merge_columns,
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.generic_master_file = Path(
            "pharma_ai/database/medicine/"
            "generic_master.csv"
        )

        self.generic_df = pd.DataFrame()
        self.master_df = pd.DataFrame()

        self.logger.info(
            "%s initialized.",
            self.__class__.__name__,
        )
    
    def _load_generic_master(self):
        """
        Load Generic Master.
        """

        self.logger.info(
            "Loading Generic Master..."
        )

        self.generic_df = pd.read_csv(
            self.generic_master_file
        )

        self.logger.info(
            "Loaded %d generic records.",
            len(self.generic_df),
        )

    def _load_existing_master(self):
        """
        Load existing master file.
        """

        self.logger.info(
            "Loading existing master..."
        )

        if self.master_file.exists():

            self.master_df = pd.read_csv(
                self.master_file
            )

            self.logger.info(
                "Existing master loaded (%d records).",
                len(self.master_df),
            )

        else:

            self.master_df = pd.DataFrame()

            self.logger.info(
                "Master file not found. "
                "New master will be created."
            )

    def _load_dependencies(self):
        """
        Load all external dependencies.
        """

        self._load_existing_master()

        self._load_generic_master()
    
    
    def _validate_generic_mapping(self):
        """
        Validate Generic Mapping.
        """

        missing_generic = self.df[
            self.df["Generic_ID"].isna()
        ]

        if not missing_generic.empty:

            raise ValueError(
                "Generic not found in "
                "generic_master.csv:\n"
                f"{missing_generic[['Generic_Name']]}"
            )

    def _map_generic_ids(self):
        """
        Map Generic_Name to Generic_ID.
        """

        self.logger.info(
            "Mapping Generic IDs..."
        )

        generic_map = dict(
            zip(
                self.generic_df["Generic_Name"],
                self.generic_df["Generic_ID"],
            )
        )

        self.df["Generic_ID"] = (
            self.df["Generic_Name"].map(
                generic_map
            )
        )

        self._validate_generic_mapping()

        self.logger.info(
            "Generic mapping completed."
        )

    def _prepare_dataframe(self):
        """
        Prepare dataframe before ID generation.
        """

        self._map_generic_ids()

        if "Generic_Name" in self.df.columns:

            self.df.drop(
                columns=["Generic_Name"],
                inplace=True,
            )

        self.logger.info(
            "Dataframe prepared."
        )

    def _add_metadata(self):
        """
        Add standard metadata.
        """

        self.logger.info(
            "Adding metadata..."
        )

        timestamp = pd.Timestamp.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.df["created_at"] = timestamp
        self.df["updated_at"] = timestamp
        self.df["version"] = "1.0"

        self.logger.info(
            "Metadata added successfully."
        )

    def _merge_master(self):
        """
        Merge new data with existing master.
        """

        self.logger.info(
            "Merging master data..."
        )

        if self.master_df.empty:

            final_df = self.df.copy()

        else:

            final_df = pd.concat(
                [
                    self.master_df,
                    self.df,
                ],
                ignore_index=True,
            )

            final_df.drop_duplicates(
                subset=self.MERGE_COLUMNS,
                keep="last",
                inplace=True,
            )

        final_df.to_csv(
            self.master_file,
            index=False,
        )

        self.logger.info(
            "Master saved successfully (%d records).",
            len(final_df),
        )

    def _pre_generate_ids(self):
        """
        Hook executed before child ID generation.

        Child builders normally call this first.
        """

        self._load_dependencies()

        self._prepare_dataframe()   

    def prepare_generic_clinical_data(self):
        """
        Common preparation pipeline for
        Generic-ID based clinical builders.
        """

        self._load_dependencies()

        self._prepare_dataframe()

        self.logger.info(
            "Generic clinical data prepared."
        )
