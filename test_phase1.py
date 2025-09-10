# Quick test for our configuration loader
from src.config_loader import load_config, get_config_value

def test_config_loading():
    """Test that we can load configuration properly."""
    try:
        config = load_config()
        
        print("✅ Configuration loaded successfully!")
        print(f"Polling interval: {config.get('polling_interval')}")
        print(f"Data sources count: {len(config.get('data_sources', []))}")
        print(f"Logz.io host: {get_config_value(config, 'logz_io.host')}")
        
        # Check each data source (handle different source types)
        for source in config.get('data_sources', []):
            source_type = source['type']
            enabled = source['enabled']
            
            if source_type == 'csv':
                file_path = source.get('file_path', 'N/A')
                print(f"- {source_type}: file='{file_path}', enabled: {enabled}")
            else:
                cities_count = len(source.get('cities', []))
                print(f"- {source_type}: {cities_count} cities, enabled: {enabled}")
        
        # Test robustness settings
        timeout = get_config_value(config, 'network.request_timeout')
        print(f"Request timeout: {timeout}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_config_loading()
    if success:
        print("\n🎉 Phase 1 complete! Ready for data sources.")
    else:
        print("\n🔧 Fix configuration issues before proceeding.")