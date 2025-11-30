import requests
from api_config import APIConfig

class WeatherAPI:
    """Class to handle weather data using OpenWeather API"""
    
    def __init__(self):
        self.base_url = APIConfig.OPENWEATHER_BASE_URL
        self.api_key = APIConfig.OPENWEATHER_API_KEY
    
    def get_current_weather(self, city):
        """Get current weather for a city"""
        endpoint = f"{self.base_url}/weather"
        
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Use Celsius
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_current_weather(data)
        except requests.exceptions.RequestException as e:
            print(f"Weather fetch failed: {e}")
            return {}
    
    def get_forecast(self, city, days=5):
        """Get weather forecast for a city"""
        endpoint = f"{self.base_url}/forecast"
        
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',  # Use Celsius
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_forecast(data)
        except requests.exceptions.RequestException as e:
            print(f"Weather forecast fetch failed: {e}")
            return []
    
    def _parse_current_weather(self, data):
        """Parse current weather data from API response"""
        weather_info = {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': data.get('main', {}).get('temp'),
            'feels_like': data.get('main', {}).get('feels_like'),
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'description': data.get('weather', [{}])[0].get('description'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'visibility': data.get('visibility'),
            'sunrise': data.get('sys', {}).get('sunrise'),
            'sunset': data.get('sys', {}).get('sunset')
        }
        
        return weather_info
    
    def _parse_forecast(self, data):
        """Parse weather forecast data from API response"""
        forecasts = []
        
        if 'list' in data:
            for item in data['list']:
                forecast = {
                    'datetime': item.get('dt'),
                    'temperature': item.get('main', {}).get('temp'),
                    'min_temp': item.get('main', {}).get('temp_min'),
                    'max_temp': item.get('main', {}).get('temp_max'),
                    'humidity': item.get('main', {}).get('humidity'),
                    'description': item.get('weather', [{}])[0].get('description'),
                    'wind_speed': item.get('wind', {}).get('speed'),
                }
                forecasts.append(forecast)
        
        return forecasts

# Example usage
if __name__ == "__main__":
    weather_api = WeatherAPI()
    
    # Get current weather
    current_weather = weather_api.get_current_weather("Paris")
    print("Current Weather:")
    print(f"City: {current_weather.get('city')}")
    print(f"Temperature: {current_weather.get('temperature')}°C")
    print(f"Description: {current_weather.get('description')}")
    
    # Get forecast
    forecast = weather_api.get_forecast("Paris", days=3)
    print("\n3-Day Forecast:")
    for i, day in enumerate(forecast[::8]):  # Show every 8th item (once per day)
        if i < 3:  # Show first 3 days
            print(f"Date: {day.get('datetime')}, Temp: {day.get('temperature')}°C, "
                  f"Description: {day.get('description')}")