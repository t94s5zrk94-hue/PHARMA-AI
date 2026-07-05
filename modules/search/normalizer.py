import unicodedata
import re

class Normalizer:
    """Handles query cleanup and normalization for search."""
    
    @staticmethod
    def normalize(query: str) -> str:
        if not query:
            return ""
        
        # 1. Unicode normalization
        query = unicodedata.normalize('NFKC', query)
        
        # 2. Lowercase and strip
        query = query.lower().strip()
        
        # 3. Remove extra spaces
        query = re.sub(r'\s+', ' ', query)
        
        # 4. Remove unwanted punctuation (keep essential chars)
        # Note: Keep digits/letters, remove special chars
        query = re.sub(r'[^a-z0-9\u0a80-\u0aff\s]', '', query) 
        
        return query