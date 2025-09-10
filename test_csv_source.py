# Test CSV data source functionality
from src.config_loader import load_config
from src.data_sources import fetch_source_data

def test_csv_source():
    """Test that we can read data from CSV file."""
    try:
        # Load configuration
        config = load_config()
        
        # Find the CSV source in config
        csv_source = None
        for source in config.get('data_sources', []):
            if source.get('type') == 'csv':
                csv_source = source
                break
        
        if not csv_source:
            print("❌ No CSV source found in configuration")
            return False
        
        print(f"📁 Testing CSV source: {csv_source.get('file_path')}")
        
        # Fetch data from CSV
        data = fetch_source_data(csv_source)
        
        print(f"✅ Successfully read {len(data)} records from CSV")
        
        # Display the data
        for i, record in enumerate(data, 1):
            city = record.get('city')
            temp = record.get('temperature')
            desc = record.get('description')
            source = record.get('source_provider')
            print(f"  {i}. {city}: {temp}°C, {desc} (source: {source})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing CSV source: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_csv_source()
    if success:
        print("\n🎉 CSV source working! Ready for API sources.")
    else:
        print("\n🔧 Fix CSV source before proceeding.")