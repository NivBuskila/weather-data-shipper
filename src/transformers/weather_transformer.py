from typing import List, Dict, Any

def transform_weather_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform raw weather data from all sources into unified JSON format.
    
    Args:
        raw_data: List of raw data dictionaries from various sources
        
    Returns:
        List of transformed dictionaries in unified format
    """
    transformed_data = []
    
    for record in raw_data:
        try:
            transformed_record = transform_single_record(record)
            if transformed_record:  # Only add valid records
                transformed_data.append(transformed_record)
        except Exception as e:
            print(f"⚠️  Warning: Skipping invalid record due to transformation error: {e}")
            # Skip invalid records as per our robustness config
            continue
    
    return transformed_data

def transform_single_record(raw_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a single raw weather record into unified format.
    
    Expected output format:
    {
        "city": "Berlin",
        "temperature_celsius": 22.86,
        "description": "clear sky",
        "source_provider": "openweathermap"
    }
    
    Args:
        raw_record: Single raw data dictionary
        
    Returns:
        Transformed dictionary in unified format
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Extract required fields
    city = raw_record.get('city')
    temperature = raw_record.get('temperature')
    description = raw_record.get('description')
    source_provider = raw_record.get('source_provider')
    
    # Validate required fields
    if not city:
        raise ValueError("Missing required field: city")
    if temperature is None:
        raise ValueError("Missing required field: temperature")
    if not description:
        raise ValueError("Missing required field: description")
    if not source_provider:
        raise ValueError("Missing required field: source_provider")
    
    # Convert temperature to float (ensure it's a double/float type)
    try:
        temperature_celsius = float(temperature)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid temperature value: {temperature}")
    
    # Create unified format
    unified_record = {
        "city": str(city).strip(),
        "temperature_celsius": temperature_celsius,
        "description": str(description).strip(),
        "source_provider": str(source_provider).strip()
    }
    
    return unified_record

def validate_transformed_data(transformed_data: List[Dict[str, Any]]) -> bool:
    """
    Validate that all transformed data follows the expected format.
    
    Args:
        transformed_data: List of transformed records
        
    Returns:
        True if all data is valid, False otherwise
    """
    required_fields = ["city", "temperature_celsius", "description", "source_provider"]
    
    for i, record in enumerate(transformed_data):
        # Check all required fields exist
        for field in required_fields:
            if field not in record:
                print(f"❌ Record {i+1} missing field: {field}")
                return False
        
        # Check data types
        if not isinstance(record["city"], str):
            print(f"❌ Record {i+1}: 'city' must be string")
            return False
        if not isinstance(record["temperature_celsius"], (int, float)):
            print(f"❌ Record {i+1}: 'temperature_celsius' must be number")
            return False
        if not isinstance(record["description"], str):
            print(f"❌ Record {i+1}: 'description' must be string")
            return False
        if not isinstance(record["source_provider"], str):
            print(f"❌ Record {i+1}: 'source_provider' must be string")
            return False
    
    return True