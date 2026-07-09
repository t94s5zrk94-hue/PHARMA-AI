import time
from datetime import datetime

import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_mapping_id
from pharma_ai.core.constants import BUILDER_VERSION


class GenericATCMappingBuilder(BaseBuilder):

    OUTPUT_COLUMNS = [
    "Mapping_ID",
    "Generic_ID",
    "ATC_ID",
    "Is_Primary",
    "created_at",
    "updated_at",
    "source",
    "version",
    "Status",
    ]

    def __init__(self):

        super().__init__(
            input_file="pharma_ai/database/medicine/generic_master.csv",
            output_path="pharma_ai/database/mapping/generic_atc_mapping.csv",
            required_columns=[],
        )

        self.generic_df = pd.DataFrame()
        self.atc_df = pd.DataFrame()
        self.mapping_df = pd.DataFrame()
    
    def _load_master(self):
        """
        Load Generic and ATC master tables.
        """

        self.logger.info("Loading master tables...")

    # Generic Master
        self.generic_df = pd.read_csv(
        "pharma_ai/database/medicine/generic_master.csv",
        dtype=str,
    )

    # ATC Master
        self.atc_df = pd.read_csv(
        "pharma_ai/database/atc/atc_master.csv",
        dtype=str,
    )

        self.logger.info(
        "Generic Master: %d records | ATC Master: %d records",
        len(self.generic_df),
        len(self.atc_df),
    )

    def _create_mapping(self) -> pd.DataFrame:
        """
        Create Generic ↔ ATC relationship table.
        """

        self.logger.info("Creating Generic-ATC mapping...")

        generic_df = self.generic_df.copy()
        atc_df = self.atc_df.copy()

        generic_df["match_name"] = (
        generic_df["Standardized_Name"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

        atc_df["match_name"] = (
        atc_df["ATC_Name"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

        mapping_df = generic_df.merge(
        atc_df,
        on="match_name",
        how="inner",
    )

        mapping_df = mapping_df[
        [
            "Generic_ID",
            "ATC_ID",
        ]
        ].copy()

        self.mapping_df = mapping_df

        self.logger.info(
        "Created %d mappings.",
        len(mapping_df),
    )

        return mapping_df

    def _generate_mapping_ids(
        self,
        mapping_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate sequential Mapping_ID values.
        """

        self.logger.info("Generating Mapping IDs...")

        if self.output_path.exists():

            master_df = pd.read_csv(
            self.output_path,
            dtype=str,
        )

            if master_df.empty:
                last_id = None
            else:
               last_id = master_df["Mapping_ID"].iloc[-1]

        else: 
            last_id = None

        mapping_df["Mapping_ID"] = get_next_mapping_id(
            last_id,
            count=len(mapping_df),
    )

        self.logger.info(
            "Generated %d Mapping IDs.",
            len(mapping_df),
    )

        return mapping_df    
    
    def _merge_master(
        self,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge new mappings with existing mapping master.
        """

        self.logger.info("Merging Generic-ATC mapping master...")

        if self.output_path.exists():

            master_df = pd.read_csv(
            self.output_path,
            dtype=str,
        )

        else:

            self.logger.info(
                "No existing mapping master found."
        )

            return new_df

        final_df = pd.concat(
            [master_df, new_df],
            ignore_index=True,
    )

        final_df = final_df.drop_duplicates(
            subset=["Generic_ID", "ATC_ID"],
            keep="first",
    )

        self.logger.info(
            "Existing=%d | New=%d | Final=%d",
            len(master_df),
            len(new_df),
            len(final_df),
    )

        return final_df
    
    def _load_existing_mapping(self) -> pd.DataFrame:
        """
        Load existing Generic-ATC mapping master.
        """

        self.logger.info("Loading existing mapping master...")

        if self.output_path.exists():

            existing_df = pd.read_csv(
            self.output_path,
            dtype=str,
        )

            self.logger.info(
            "Loaded %d existing mappings.",
            len(existing_df),
        )

            return existing_df

        self.logger.info(
            "No existing mapping master found."
    )

        return pd.DataFrame(
            columns=self.OUTPUT_COLUMNS,
    )

    def _assign_mapping_ids(
        self,
        existing_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Preserve existing Mapping_IDs and assign IDs only to new mappings.
        """
        self.logger.info("Assigning Mapping IDs...")

    # First run
        if existing_df.empty:
            new_df["Mapping_ID"] = get_next_mapping_id(
            None,
            count=len(new_df),
        )
            return new_df

        existing_keys = existing_df[
            ["Generic_ID", "ATC_ID", "Mapping_ID"]
        ] 
        merged = new_df.merge(
                existing_keys,
            on=["Generic_ID", "ATC_ID"],
            how="left",
        )
        new_mask = merged["Mapping_ID"].isna()

    # No new mappings
        if not new_mask.any():
            self.logger.info("No new mappings found.")
            return merged

        last_id = existing_df["Mapping_ID"].dropna().iloc[-1]

        new_ids = get_next_mapping_id(
            last_id,
            count=int(new_mask.sum()),
        )
        merged.loc[new_mask, "Mapping_ID"] = new_ids

        self.logger.info(
        "Existing=%d | New=%d",
        (~new_mask).sum(),
        new_mask.sum(),
        )

        return merged
    
    def _add_metadata(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add production metadata to mapping records.
        """

        self.logger.info("Adding metadata...")

        current_time = datetime.now().isoformat()

        df["Is_Primary"] = True

        df["created_at"] = current_time

        df["updated_at"] = current_time

        df["source"] = "WHO"

        df["version"] = BUILDER_VERSION

        df["Status"] = "Active"

        return df
    
    def build(self) -> dict:
        """
        Build Generic ↔ ATC mapping master.
        """

        start_time = time.time()

        self.logger.info(
            "Starting Generic ATC Mapping Builder..."
        )

    # Step 1
        self._load_master()

    # Step 2
        mapping_df = self._create_mapping()

        input_count = len(mapping_df)

    # Step 3
        existing_df = self._load_existing_mapping()

   # Step 4
        new_df = self._assign_mapping_ids(
        existing_df,
        mapping_df,
    )

    # Step 5
        new_df = self._add_metadata(new_df)

    # Step 6
        final_df = pd.concat(
        [existing_df, new_df],
        ignore_index=True,
    )

        final_df = final_df.drop_duplicates(
        subset=["Generic_ID", "ATC_ID"],
        keep="first",
    )
    # Step 7
        final_df = final_df[self.OUTPUT_COLUMNS]

    # Step 8
        self.save_csv(final_df)

        self.logger.info(
            "Generic ATC Mapping Builder completed successfully."
        )

        return self.get_summary(
        start_time,
        input_count,
        len(final_df),
        0,
        0,
        0,
        "SUCCESS",
    )

if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    builder = GenericATCMappingBuilder()

    summary = builder.build()

    print("\n=== Generic ATC Mapping Builder Summary ===")
    print(summary)    