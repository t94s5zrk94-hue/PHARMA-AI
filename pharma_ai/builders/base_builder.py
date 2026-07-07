import logging
import time
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

# Constants
ENCODING = "utf-8"
SEPARATOR = ","

class BaseBuilder:
    def __init__(self, input_file: str, output_path: str, required_columns: List[str]):
        self.input_path = Path(input_file)
        self.output_path = Path(output_path)
        self.required_columns = required_columns
        self.df: pd.DataFrame = pd.DataFrame()
        self.logger = logging.getLogger("pharma_ai.builder")

    def validate_input(self) -> None:
        """Validate input file existence and size."""
        if not self.input_path.exists():
            self.logger.error(f"Input file not found: {self.input_path}")
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        if self.input_path.stat().st_size == 0:
            self.logger.error("Input file is empty.")
            raise ValueError("Input file is empty.")
        
        self.logger.info("Input file validation passed.")

    def load_csv(self) -> pd.DataFrame:
        """Read CSV, strip column names, and enforce string types for IDs."""
        try:
            # dtype=str prevents IDs from becoming integers (e.g., 00123 -> 123)
            self.df = pd.read_csv(self.input_path, sep=SEPARATOR, encoding=ENCODING, dtype=str)
            
            # Clean column names: Strip leading/trailing spaces
            self.df.columns = self.df.columns.str.strip()
            
            # Check for duplicate column names
            if self.df.columns.duplicated().any():
                duplicated = self.df.columns[self.df.columns.duplicated()].tolist()
                self.logger.error(f"Duplicate column names found: {duplicated}")
                raise ValueError(f"Duplicate column names detected: {duplicated}")

            if self.df.empty:
                self.logger.error("DataFrame is empty after loading.")
                raise ValueError("The provided CSV file contains no data.")
                
            return self.df
        except Exception as e:
            self.logger.error(f"Error loading CSV: {str(e)}")
            raise

    def validate_columns(self, df: pd.DataFrame) -> None:
        """Ensure all required columns exist in the DataFrame."""
        missing = [col for col in self.required_columns if col not in df.columns]
        if missing:
            self.logger.error(f"Missing required columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")
        self.logger.info("Column validation passed.")

    def save_csv(self, final_df: pd.DataFrame) -> None:
        """Save the processed DataFrame with pathlib."""
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            final_df.to_csv(self.output_path, index=False, sep=SEPARATOR, encoding=ENCODING)
            self.logger.info(f"File saved successfully at: {self.output_path}")
        except Exception as e:
            self.logger.error(f"Error saving CSV: {str(e)}")
            raise

    def get_summary(self, start_time: float, input_count: int, output_count: int, 
                    dups_removed: int, skipped: int, failed: int, status: str) -> Dict[str, Any]:
        """Return processing summary."""
        duration = time.time() - start_time
        summary = {
            "execution_time_sec": round(duration, 4),
            "input_records": input_count,
            "output_records": output_count,
            "duplicates_removed": dups_removed,
            "skipped": skipped,
            "failed": failed,
            "status": status
        }
        self.logger.info(f"Builder Summary: {summary}")
        return summary