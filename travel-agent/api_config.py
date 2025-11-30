import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIConfig:
    """Configuration class for API keys and settings"""
    
    # Amadeus API Configuration
    AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY', '')
    AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET', '')
    AMADEUS_BASE_URL = 'https://test.api.amadeus.com/v1'  # Use test environment for development
    
    # RapidAPI Configuration
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
    RAPIDAPI_HOTELS_URL = 'https://hotels4.p.rapidapi.com'
    
    # OpenWeather API Configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    OPENWEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5'
    
    # Validation
    @classmethod
    def validate_config(cls):
        """Validate that all required API keys are present"""
        required_keys = [
            cls.AMADEUS_API_KEY,
            cls.AMADEUS_API_SECRET,
            cls.RAPIDAPI_KEY,
            cls.OPENWEATHER_API_KEY
        ]
        
        for key in required_keys:
            if not key or key == 'your_api_key_here':
                raise ValueError(f"Missing required API key: {key}")
        
        return True