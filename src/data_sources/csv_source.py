import csv
from typing import List, Dict, Any

def fetch_csv_data(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Read weather data from CSV file.
    Expected CSV format: city,temperature,description
    
    Args:
        source_config: Configuration dict containing 'file_path', 'enabled', etc.
    
    Returns:
        List of raw data dictionaries
    """
    # Check if source is enabled
    if not source_config.get('enabled', True):
        return []
    
    file_path = source_config.get('file_path')
    if not file_path:
        raise ValueError("CSV source requires 'file_path' in configuration")
    
    try:
        data = []
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Add source type to raw data
                row['source_provider'] = source_config.get('type', 'csv')
                data.append(row)
        
        return data
        
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file {file_path}: {e}")