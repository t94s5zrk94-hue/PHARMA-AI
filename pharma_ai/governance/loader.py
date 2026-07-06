"""
Policy loader module.
Updated to support nested metadata structure in configuration.
"""

from pathlib import Path
from datetime import datetime
import yaml
from .models import PolicyConfig, QualityWeights, Thresholds
from .exceptions import PolicyLoadError, ConfigurationParseError

# Required top-level keys
REQUIRED_SECTIONS = ('metadata', 'weights', 'thresholds', 'release', 'audit', 'config_hash')

class PolicyLoader:
    """
    Loads and parses PolicyConfig from nested YAML structure.
    """

    @staticmethod
    def load(path: Path) -> PolicyConfig:
        """
        Loads YAML and maps it to PolicyConfig, navigating nested metadata.
        """
        if not path.exists() or not path.is_file():
            raise PolicyLoadError(f"Policy file not found: {path}", "GOV-002")

        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            if data is None:
                raise ConfigurationParseError("Policy file is empty", "GOV-001")
            
            # 1. Structural Validation
            for section in REQUIRED_SECTIONS:
                if section not in data:
                    raise ConfigurationParseError(f"Missing required section: {section}", "GOV-001")

            # 2. Extract nested data
            metadata = data['metadata']
            
            # 3. Map to Domain Models
            return PolicyConfig(
                version=metadata['version'],
                weights=QualityWeights(**data['weights']),
                thresholds=Thresholds(**data['thresholds']),
                effective_date=datetime.fromisoformat(metadata['effective_date']),
                config_hash=data['config_hash']
            )

        except (KeyError, TypeError) as e:
            raise ConfigurationParseError(f"Schema mismatch/Nested key missing: {str(e)}", "GOV-001") from e
        except ValueError as e:
            raise ConfigurationParseError(f"Invalid data format: {str(e)}", "GOV-001") from e
        except yaml.YAMLError as e:
            raise ConfigurationParseError(f"YAML parsing failed: {str(e)}", "GOV-001") from e
        except Exception as e:
            raise PolicyLoadError(f"Unexpected loader failure: {str(e)}", "GOV-002", {"exception": type(e).__name__}) from e