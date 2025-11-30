import requests
from api_config import APIConfig

class RapidAPIHotels:
    """Class to handle hotel data using RapidAPI Hotels API"""
    
    def __init__(self):
        self.base_url = APIConfig.RAPIDAPI_HOTELS_URL
        self.api_key = APIConfig.RAPIDAPI_KEY
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
    
    def search_locations(self, query):
        """Search for hotel locations by city name"""
        endpoint = f"{self.base_url}/locations/search"
        
        params = {
            'query': query,
            'locale': 'en_US'
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_location_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Location search failed: {e}")
            return []
    
    def get_hotel_list(self, destination_id, checkin_date, checkout_date, adults=2, rooms=1):
        """Get list of hotels for a destination"""
        endpoint = f"{self.base_url}/properties/list"
        
        params = {
            'destinationId': destination_id,
            'pageNumber': '1',
            'checkIn': checkin_date,
            'checkOut': checkout_date,
            'adults1': adults,
            'rooms1': rooms,
            'sortOrder': 'PRICE',
            'locale': 'en_US',
            'currency': 'USD'
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_hotel_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Hotel search failed: {e}")
            return []
    
    def get_hotel_details(self, hotel_id):
        """Get detailed information about a specific hotel"""
        endpoint = f"{self.base_url}/properties/get-details"
        
        params = {
            'id': hotel_id,
            'checkIn': '2023-12-01',
            'checkOut': '2023-12-02',
            'adults1': '2',
            'locale': 'en_US',
            'currency': 'USD'
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_hotel_details(data)
        except requests.exceptions.RequestException as e:
            print(f"Hotel details fetch failed: {e}")
            return {}
    
    def _parse_location_data(self, data):
        """Parse location data from API response"""
        locations = []
        
        if 'suggestions' in data:
            for suggestion in data['suggestions']:
                if suggestion.get('group') == 'CITY_GROUP':
                    for entity in suggestion.get('entities', []):
                        location = {
                            'dest_id': entity.get('destinationId'),
                            'name': entity.get('name'),
                            'country': entity.get('countryName')
                        }
                        locations.append(location)
        
        return locations
    
    def _parse_hotel_data(self, data):
        """Parse hotel data from API response"""
        hotels = []
        
        if 'data' in data and 'body' in data['data'] and 'searchResults' in data['data']['body']:
            results = data['data']['body']['searchResults']['results']
            
            for hotel in results:
                hotel_info = {
                    'id': hotel.get('id'),
                    'name': hotel.get('name'),
                    'address': hotel.get('address', {}).get('streetAddress', ''),
                    'city': hotel.get('address', {}).get('cityName', ''),
                    'country': hotel.get('address', {}).get('countryName', ''),
                    'price': hotel.get('ratePlan', {}).get('price', {}).get('current', 'N/A'),
                    'currency': 'USD',
                    'rating': hotel.get('starRating', 'N/A'),
                    'review_score': hotel.get('guestReviews', {}).get('score', 'N/A'),
                    'image_url': hotel.get('thumbNailUrl', ''),
                    'amenities': hotel.get('amenities', [])
                }
                hotels.append(hotel_info)
        
        return hotels
    
    def _parse_hotel_details(self, data):
        """Parse detailed hotel information from API response"""
        if 'data' in data and 'body' in data['data']:
            hotel = data['data']['body']
            return {
                'id': hotel.get('id'),
                'name': hotel.get('name'),
                'description': hotel.get('description', ''),
                'policies': hotel.get('policies', {}),
                'room_types': hotel.get('roomTypes', []),
                'property_amenities': hotel.get('propertyContent', {}).get('amenities', []),
                'location': hotel.get('location', {})
            }
        
        return {}

# Example usage
if __name__ == "__main__":
    hotel_api = RapidAPIHotels()
    
    # Search for locations
    locations = hotel_api.search_locations("Paris")
    print(f"Found {len(locations)} locations")
    
    if locations:
        # Get hotels for the first location
        hotels = hotel_api.get_hotel_list(
            destination_id=locations[0]['dest_id'],
            checkin_date='2023-12-01',
            checkout_date='2023-12-05',
            adults=2
        )
        
        print(f"Found {len(hotels)} hotels")
        for hotel in hotels[:2]:  # Show first 2 results
            print(f"Hotel: {hotel['name']}, Price: {hotel['price']}")