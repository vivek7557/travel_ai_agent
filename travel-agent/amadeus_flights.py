import requests
import json
from datetime import datetime
from api_config import APIConfig

class AmadeusFlightsAPI:
    """Class to handle flight data using Amadeus API"""
    
    def __init__(self):
        self.base_url = APIConfig.AMADEUS_BASE_URL
        self.api_key = APIConfig.AMADEUS_API_KEY
        self.api_secret = APIConfig.AMADEUS_API_SECRET
        self.access_token = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Amadeus API to get access token"""
        auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        
        try:
            response = requests.post(auth_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            raise
    
    def search_flights(self, origin, destination, departure_date, return_date=None, adults=1):
        """Search for flights using Amadeus API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': adults,
            'max': 10
        }
        
        if return_date:
            params['returnDate'] = return_date
        
        url = f"{self.base_url}/shopping/flight-offers"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_flight_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Flight search failed: {e}")
            return []
    
    def _parse_flight_data(self, data):
        """Parse flight data from Amadeus API response"""
        flights = []
        
        if 'data' in data:
            for flight_offer in data['data']:
                flight_info = {
                    'id': flight_offer.get('id'),
                    'price': flight_offer.get('price', {}).get('total', 'N/A'),
                    'currency': flight_offer.get('price', {}).get('currency', 'USD'),
                    'itineraries': []
                }
                
                for itinerary in flight_offer.get('itineraries', []):
                    segments = []
                    for segment in itinerary.get('segments', []):
                        segment_info = {
                            'carrier': segment.get('carrierCode'),
                            'number': segment.get('number'),
                            'origin': segment.get('departure', {}).get('iataCode'),
                            'destination': segment.get('arrival', {}).get('iataCode'),
                            'departure_time': segment.get('departure', {}).get('at'),
                            'arrival_time': segment.get('arrival', {}).get('at'),
                            'duration': segment.get('duration')
                        }
                        segments.append(segment_info)
                    
                    flight_info['itineraries'].append({
                        'duration': itinerary.get('duration'),
                        'segments': segments
                    })
                
                flights.append(flight_info)
        
        return flights

# Example usage
if __name__ == "__main__":
    # Initialize the API client
    flight_api = AmadeusFlightsAPI()
    
    # Search for flights
    flights = flight_api.search_flights(
        origin="NYC",
        destination="PAR",
        departure_date="2023-12-25",
        adults=2
    )
    
    print(f"Found {len(flights)} flight options")
    for flight in flights[:2]:  # Show first 2 results
        print(json.dumps(flight, indent=2))