import unittest
from src.transformers.weather_transformer import (
    transform_single_record, 
    transform_weather_data, 
    validate_transformed_data
)

class TestWeatherTransformer(unittest.TestCase):
    """Unit tests for weather data transformation logic."""
    
    def test_transform_single_record_valid_data(self):
        """Test transformation of valid raw data record."""
        # Test data from different sources
        test_cases = [
            # OpenWeatherMap format
            {
                'city': 'Berlin',
                'temperature': 22.86,
                'description': 'clear sky',
                'source_provider': 'openweathermap'
            },
            # WeatherAPI format  
            {
                'city': 'Sydney',
                'temperature': 14.1,
                'description': 'Light rain',
                'source_provider': 'weatherapi'
            },
            # CSV format
            {
                'city': 'Tokyo',
                'temperature': '25.3',  # String temperature (should be converted)
                'description': 'Sunny',
                'source_provider': 'csv'
            }
        ]
        
        for raw_record in test_cases:
            with self.subTest(raw_record=raw_record):
                result = transform_single_record(raw_record)
                
                # Check unified format structure
                self.assertIn('city', result)
                self.assertIn('temperature_celsius', result)
                self.assertIn('description', result)
                self.assertIn('source_provider', result)
                
                # Check data types
                self.assertIsInstance(result['city'], str)
                self.assertIsInstance(result['temperature_celsius'], float)
                self.assertIsInstance(result['description'], str)
                self.assertIsInstance(result['source_provider'], str)
                
                # Check values
                self.assertEqual(result['city'], raw_record['city'])
                self.assertEqual(result['temperature_celsius'], float(raw_record['temperature']))
                self.assertEqual(result['description'], raw_record['description'])
                self.assertEqual(result['source_provider'], raw_record['source_provider'])
    
    def test_transform_single_record_missing_fields(self):
        """Test transformation fails gracefully with missing required fields."""
        test_cases = [
            {'temperature': 20.0, 'description': 'sunny', 'source_provider': 'test'},  # Missing city
            {'city': 'Berlin', 'description': 'sunny', 'source_provider': 'test'},     # Missing temperature
            {'city': 'Berlin', 'temperature': 20.0, 'source_provider': 'test'},       # Missing description
            {'city': 'Berlin', 'temperature': 20.0, 'description': 'sunny'},          # Missing source_provider
        ]
        
        for invalid_record in test_cases:
            with self.subTest(invalid_record=invalid_record):
                with self.assertRaises(ValueError):
                    transform_single_record(invalid_record)
    
    def test_transform_single_record_invalid_temperature(self):
        """Test transformation handles invalid temperature values."""
        invalid_temperature_cases = [
            {'city': 'Berlin', 'temperature': 'not_a_number', 'description': 'sunny', 'source_provider': 'test'},
            {'city': 'Berlin', 'temperature': None, 'description': 'sunny', 'source_provider': 'test'},
            {'city': 'Berlin', 'temperature': [], 'description': 'sunny', 'source_provider': 'test'},
        ]
        
        for invalid_record in invalid_temperature_cases:
            with self.subTest(invalid_record=invalid_record):
                with self.assertRaises(ValueError):
                    transform_single_record(invalid_record)

                    
    
    def test_transform_weather_data_mixed_valid_invalid(self):
        """Test transformation of list with both valid and invalid records."""
        mixed_data = [
            # Valid record
            {'city': 'Berlin', 'temperature': 22.5, 'description': 'sunny', 'source_provider': 'test'},
            # Invalid record (missing city) - should be skipped
            {'temperature': 20.0, 'description': 'cloudy', 'source_provider': 'test'},
            # Valid record
            {'city': 'Tokyo', 'temperature': '15.0', 'description': 'rainy', 'source_provider': 'test'},
        ]
        
        result = transform_weather_data(mixed_data)
        
        # Should return only the 2 valid records
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['city'], 'Berlin')
        self.assertEqual(result[1]['city'], 'Tokyo')
    
    def test_validate_transformed_data_valid(self):
        """Test validation of properly transformed data."""
        valid_data = [
            {
                "city": "Berlin",
                "temperature_celsius": 22.86,
                "description": "clear sky",
                "source_provider": "openweathermap"
            },
            {
                "city": "Tokyo", 
                "temperature_celsius": 15.5,
                "description": "rainy",
                "source_provider": "weatherapi"
            }
        ]
        
        self.assertTrue(validate_transformed_data(valid_data))
    
    def test_validate_transformed_data_invalid(self):
        """Test validation catches invalid transformed data."""
        invalid_cases = [
            # Missing field
            [{"city": "Berlin", "temperature_celsius": 20.0, "description": "sunny"}],
            # Wrong data type for temperature
            [{"city": "Berlin", "temperature_celsius": "20.0", "description": "sunny", "source_provider": "test"}],
            # Wrong data type for city
            [{"city": 123, "temperature_celsius": 20.0, "description": "sunny", "source_provider": "test"}],
        ]
        
        for invalid_data in invalid_cases:
            with self.subTest(invalid_data=invalid_data):
                self.assertFalse(validate_transformed_data(invalid_data))

if __name__ == '__main__':
    # Run the tests
    unittest.main()