import requests
from typing import List, Dict, Any

def fetch_weatherapi_data(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch weather data from WeatherAPI.com.
    
    Args:
        source_config: Configuration dict containing 'cities', 'api_key', etc.
    
    Returns:
        List of raw data dictionaries
    """
    # Check if source is enabled
    if not source_config.get('enabled', True):
        return []
    
    api_key = source_config.get('api_key')
    cities = source_config.get('cities', [])
    
    if not api_key:
        raise ValueError("WeatherAPI source requires 'api_key'")
    
    if not cities:
        return []
    
    data = []
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    for city in cities:
        try:
            # Make API request
            params = {
                'key': api_key,
                'q': city,
                'aqi': 'no'  # We don't need air quality data
            }
            
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            weather_data = response.json()
            
            # Extract relevant data and standardize format
            record = {
                'city': weather_data['location']['name'],
                'temperature': weather_data['current']['temp_c'],
                'description': weather_data['current']['condition']['text'],
                'source_provider': 'weatherapi'
            }
            
            data.append(record)
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Warning: Failed to fetch data for {city} from WeatherAPI: {e}")
            continue
        except KeyError as e:
            print(f"⚠️  Warning: Unexpected response format for {city} from WeatherAPI: {e}")
            continue
    
    return data