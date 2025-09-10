import requests
from typing import List, Dict, Any

def fetch_openweathermap_data(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch weather data from OpenWeatherMap API.
    
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
        raise ValueError("OpenWeatherMap source requires 'api_key'")
    
    if not cities:
        return []
    
    data = []
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    for city in cities:
        try:
            # Make API request
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'  # Get temperature in Celsius
            }
            
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            weather_data = response.json()
            
            # Extract relevant data and standardize format
            record = {
                'city': weather_data.get('name', city),
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'source_provider': 'openweathermap'
            }
            
            data.append(record)
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Warning: Failed to fetch data for {city} from OpenWeatherMap: {e}")
            continue
        except KeyError as e:
            print(f"⚠️  Warning: Unexpected response format for {city} from OpenWeatherMap: {e}")
            continue
    
    return data