# Test complete data transformation pipeline
from src.config_loader import load_config
from src.data_sources import fetch_all_sources_data
from src.transformers.weather_transformer import transform_weather_data, validate_transformed_data
import json

def test_transformation_pipeline():
    """Test the complete pipeline: fetch -> transform -> validate."""
    try:
        print("🔄 Testing complete transformation pipeline...")
        
        # Step 1: Load configuration
        config = load_config()
        
        # Step 2: Fetch raw data from all sources
        print("\n📥 Fetching raw data...")
        raw_data = fetch_all_sources_data(config)
        print(f"Raw records fetched: {len(raw_data)}")
        
        # Step 3: Transform data to unified format
        print("\n🔄 Transforming data...")
        transformed_data = transform_weather_data(raw_data)
        print(f"Records after transformation: {len(transformed_data)}")
        
        # Step 4: Validate transformed data
        print("\n✅ Validating transformed data...")
        is_valid = validate_transformed_data(transformed_data)
        
        if not is_valid:
            print("❌ Transformed data validation failed")
            return False
        
        # Step 5: Display transformed data in unified format
        print("\n📋 Transformed data (unified JSON format):")
        for i, record in enumerate(transformed_data, 1):
            print(f"  {i}. {json.dumps(record, indent=2)}")
        
        # Step 6: Show what the Logz.io payload would look like
        print("\n📤 Logz.io payload format (newline-delimited JSON):")
        print("-" * 50)
        for record in transformed_data:
            print(json.dumps(record))
        print("-" * 50)
        
        print(f"\n✅ Pipeline successful! {len(transformed_data)} records ready for shipping.")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_transformation_pipeline()
    if success:
        print("\n🎉 Transformation pipeline working! Ready for data shipping.")
    else:
        print("\n🔧 Fix pipeline issues before proceeding.")