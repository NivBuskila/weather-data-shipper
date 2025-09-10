# Test all data sources
from src.config_loader import load_config
from src.data_sources import fetch_all_sources_data

def test_all_sources():
    """Test fetching data from all configured sources."""
    try:
        # Load configuration (will also load .env)
        config = load_config()
        
        print("🌍 Testing all data sources...")
        
        # Fetch data from all sources
        all_data = fetch_all_sources_data(config)
        
        print(f"\n📊 Total records fetched: {len(all_data)}")
        
        # Display all records
        for i, record in enumerate(all_data, 1):
            city = record.get('city')
            temp = record.get('temperature')
            desc = record.get('description')
            source = record.get('source_provider')
            print(f"  {i}. {city}: {temp}°C, {desc} (source: {source})")
        
        return len(all_data) > 0
        
    except Exception as e:
        print(f"❌ Error testing data sources: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_sources()
    if success:
        print("\n🎉 All data sources working! Ready for transformation.")
    else:
        print("\n🔧 Fix data source issues before proceeding.")