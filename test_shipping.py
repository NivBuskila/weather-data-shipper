# Test shipping data to Logz.io
from src.config_loader import load_config
from src.data_sources import fetch_all_sources_data
from src.transformers.weather_transformer import transform_weather_data
from src.shipper.logz_io_client import ship_with_retry

def test_shipping():
    """Test the complete pipeline including shipping to Logz.io."""
    try:
        print("🔄 Testing complete pipeline with Logz.io shipping...")
        
        # Load configuration
        config = load_config()
        
        # Fetch and transform data
        raw_data = fetch_all_sources_data(config)
        transformed_data = transform_weather_data(raw_data)
        
        print(f"📊 Ready to ship {len(transformed_data)} records")
        
        # Ship to Logz.io
        success = ship_with_retry(transformed_data, config)
        
        if success:
            print("🎉 Complete pipeline successful!")
            print("📈 Check your Logz.io dashboard for the data!")
            return True
        else:
            print("❌ Shipping failed")
            return False
            
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_shipping()