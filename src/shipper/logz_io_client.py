import requests
import json
from typing import List, Dict, Any

def ship_to_logz_io(transformed_data: List[Dict[str, Any]], logz_config: Dict[str, Any]) -> bool:
    """
    Ship transformed weather data to Logz.io listener endpoint.
    
    Args:
        transformed_data: List of records in unified JSON format
        logz_config: Logz.io configuration (host, port, token)
        
    Returns:
        True if shipping successful, False otherwise
    """
    if not transformed_data:
        print("ℹ️  No data to ship")
        return True
    
    # Extract Logz.io configuration
    host = logz_config.get('host')
    port = logz_config.get('port', 8071)
    token = logz_config.get('token')
    
    if not host or not token:
        raise ValueError("Logz.io configuration missing 'host' or 'token'")
    
    # Build endpoint URL
    url = f"https://{host}:{port}/?token={token}"
    
    # Prepare newline-delimited JSON payload
    payload_lines = []
    for record in transformed_data:
        payload_lines.append(json.dumps(record))
    
    payload = '\n'.join(payload_lines)
    
    print(f"📤 Shipping {len(transformed_data)} records to Logz.io...")
    print(f"🌐 Endpoint: {url}")
    
    try:
        # Send HTTP POST request
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            url,
            data=payload,
            headers=headers,
            timeout=30  # Use timeout from config if available
        )
        
        # Check response
        if response.status_code == 200:
            print("✅ Successfully shipped data to Logz.io!")
            return True
        else:
            print(f"❌ Logz.io responded with status {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout while shipping to Logz.io")
        return False
    except requests.exceptions.ConnectionError:
        print("🌐 Connection error while shipping to Logz.io")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed while shipping to Logz.io: {e}")
        return False

def ship_with_retry(transformed_data: List[Dict[str, Any]], config: Dict[str, Any]) -> bool:
    """
    Ship data to Logz.io with retry logic for robustness.
    
    Args:
        transformed_data: List of records in unified JSON format
        config: Full application configuration
        
    Returns:
        True if shipping successful (eventually), False if all retries failed
    """
    logz_config = config.get('logz_io', {})
    network_config = config.get('network', {})
    
    retry_attempts = network_config.get('retry_attempts', 3)
    retry_delay_base = network_config.get('retry_delay_base', 2)
    
    for attempt in range(1, retry_attempts + 1):
        print(f"🔄 Shipping attempt {attempt}/{retry_attempts}")
        
        success = ship_to_logz_io(transformed_data, logz_config)
        
        if success:
            return True
        
        if attempt < retry_attempts:
            # Exponential backoff: 2s, 4s, 8s
            delay = retry_delay_base ** attempt
            print(f"⏳ Waiting {delay}s before retry...")
            import time
            time.sleep(delay)
    
    print("❌ All shipping attempts failed")
    return False