import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

def load_config(config_file: str = "config/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file and environment variables."""
    # Load environment variables from .env file (in root directory)
    load_dotenv()
    
    # Load YAML configuration
    config = _load_yaml_config(config_file)
    
    # Apply environment variable overrides
    _apply_env_overrides(config)
    
    return config

def _load_yaml_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in configuration file: {e}")

def _apply_env_overrides(config: Dict[str, Any]) -> None:
    """Apply environment variable overrides to config."""
    # API Keys
    if openweather_key := os.getenv('OPENWEATHER_API_KEY'):
        _set_api_key(config, 'openweathermap', openweather_key)
        
    if weatherapi_key := os.getenv('WEATHERAPI_API_KEY'):
        _set_api_key(config, 'weatherapi', weatherapi_key)
    
    # Logz.io settings
    if logz_token := os.getenv('LOGZ_IO_TOKEN'):
        config.setdefault('logz_io', {})['token'] = logz_token
        
    if logz_host := os.getenv('LOGZ_IO_HOST'):
        config.setdefault('logz_io', {})['host'] = logz_host

def _set_api_key(config: Dict[str, Any], source_type: str, api_key: str) -> None:
    """Set API key for a specific data source type."""
    for source in config.get('data_sources', []):
        if source.get('type') == source_type:
            source['api_key'] = api_key

def get_config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Get a configuration value by dot notation key (e.g., 'logz_io.host')."""
    keys = key.split('.')
    value = config
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default
            
    return value