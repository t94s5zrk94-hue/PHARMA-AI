import pandas as pd

class BaseRepository:
    """
    Base Repository to handle standardized database operations.
    No business logic here, only data access and safety handling.
    """
    def __init__(self, db_instance):
        self.db = db_instance

    def find_by_column(self, df, column_name, value):
        """Standardized lookup with NaN safety and case insensitivity."""
        if df is None or column_name not in df.columns:
            return None
            
        # Using .fillna("") to prevent NaN errors and .astype(str) for uniform matching
        mask = df[column_name].fillna("").astype(str).str.lower() == str(value).lower()
        result = df[mask]
        
        return result.to_dict('records') if not result.empty else None

    def find_one(self, df, column_name, value):
        """Returns the first match as a domain dictionary."""
        results = self.find_by_column(df, column_name, value)
        return results[0] if results else None

    def get_all_records(self, df):
        """Converts entire DataFrame to list of dictionaries."""
        return df.to_dict('records') if df is not None else []

    def is_empty(self, df):
        """Utility to check dataframe status."""
        return df is None or df.empty