from typing import List, Dict, Any
from .csv_source import fetch_csv_data
from .openweathermap_source import fetch_openweathermap_data
from .weatherapi_source import fetch_weatherapi_data

def fetch_source_data(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch data from any configured source type.
    
    Args:
        source_config: Configuration dict for the data source
        
    Returns:
        List of raw data dictionaries
    """
    source_type = source_config.get('type')
    
    if source_type == 'csv':
        return fetch_csv_data(source_config)
    elif source_type == 'openweathermap':
        return fetch_openweathermap_data(source_config)
    elif source_type == 'weatherapi':
        return fetch_weatherapi_data(source_config)
    else:
        raise ValueError(f"Unknown source type: {source_type}")

def fetch_all_sources_data(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch data from all configured and enabled data sources.
    
    Args:
        config: Full application configuration
        
    Returns:
        Combined list of raw data from all sources
    """
    all_data = []
    
    for source_config in config.get('data_sources', []):
        if source_config.get('enabled', True):
            try:
                source_data = fetch_source_data(source_config)
                all_data.extend(source_data)
                print(f"✅ Fetched {len(source_data)} records from {source_config.get('type')}")
            except Exception as e:
                print(f"❌ Failed to fetch from {source_config.get('type')}: {e}")
                # Continue with other sources instead of failing completely
                continue
    
    return all_data