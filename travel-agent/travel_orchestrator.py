from amadeus_flights import AmadeusFlightsAPI
from rapidapi_hotels import RapidAPIHotels
from weather_api import WeatherAPI
import json

class TravelOrchestrator:
    """Main coordinator class that orchestrates all travel services"""
    
    def __init__(self):
        self.flight_api = AmadeusFlightsAPI()
        self.hotel_api = RapidAPIHotels()
        self.weather_api = WeatherAPI()
    
    def plan_trip(self, origin, destination, departure_date, return_date, 
                  adults=2, budget=None, rooms=1):
        """
        Plan a complete trip by coordinating all services
        """
        trip_plan = {
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'adults': adults,
            'budget': budget,
            'rooms': rooms,
            'flights': [],
            'hotels': [],
            'weather': {},
            'recommendations': []
        }
        
        # Search for flights
        print("Searching for flights...")
        try:
            flights = self.flight_api.search_flights(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults
            )
            trip_plan['flights'] = flights
            print(f"Found {len(flights)} flight options")
        except Exception as e:
            print(f"Error searching for flights: {e}")
        
        # Search for hotels
        print("Searching for hotels...")
        try:
            # First find the destination ID
            locations = self.hotel_api.search_locations(destination)
            if locations:
                destination_id = locations[0]['dest_id']
                
                # Get hotels for the destination
                hotels = self.hotel_api.get_hotel_list(
                    destination_id=destination_id,
                    checkin_date=departure_date,
                    checkout_date=return_date,
                    adults=adults,
                    rooms=rooms
                )
                trip_plan['hotels'] = hotels
                print(f"Found {len(hotels)} hotel options")
            else:
                print("Could not find destination for hotels")
        except Exception as e:
            print(f"Error searching for hotels: {e}")
        
        # Get weather information
        print("Fetching weather information...")
        try:
            weather = self.weather_api.get_current_weather(destination)
            trip_plan['weather'] = weather
            print("Weather information retrieved")
        except Exception as e:
            print(f"Error fetching weather: {e}")
        
        # Generate recommendations based on the destination
        print("Generating recommendations...")
        try:
            recommendations = self._generate_recommendations(destination, weather)
            trip_plan['recommendations'] = recommendations
            print("Recommendations generated")
        except Exception as e:
            print(f"Error generating recommendations: {e}")
        
        return trip_plan
    
    def _generate_recommendations(self, destination, weather):
        """Generate travel recommendations based on destination and weather"""
        recommendations = []
        
        # Add weather-based recommendations
        if weather:
            temp = weather.get('temperature', 0)
            description = weather.get('description', '').lower()
            
            if 'rain' in description or 'shower' in description:
                recommendations.append("Pack rain gear and waterproof clothing")
            elif temp < 10:
                recommendations.append("Pack warm clothing and layers")
            elif temp > 25:
                recommendations.append("Pack light clothing and sun protection")
        
        # Add destination-based recommendations
        popular_attractions = {
            'Paris': [
                'Visit the Eiffel Tower',
                'Explore the Louvre Museum',
                'Stroll along the Seine River',
                'Try authentic French cuisine'
            ],
            'London': [
                'Visit Buckingham Palace',
                'See Big Ben and the Houses of Parliament',
                'Explore the British Museum',
                'Take a ride on the London Eye'
            ],
            'New York': [
                'Visit Times Square',
                'Explore Central Park',
                'See the Statue of Liberty',
                'Catch a Broadway show'
            ],
            'Tokyo': [
                'Visit Shibuya Crossing',
                'Explore Asakusa and Senso-ji Temple',
                'Experience the food scene in Tsukiji',
                'Visit Tokyo Skytree'
            ]
        }
        
        if destination in popular_attractions:
            recommendations.extend(popular_attractions[destination])
        else:
            recommendations.append(f"Research popular attractions in {destination}")
            recommendations.append(f"Learn about local customs in {destination}")
        
        return recommendations
    
    def filter_by_budget(self, trip_plan, budget):
        """Filter trip options based on budget"""
        filtered_plan = trip_plan.copy()
        
        # Filter flights by budget
        if budget and trip_plan['flights']:
            filtered_flights = []
            for flight in trip_plan['flights']:
                try:
                    price = float(flight['price']) if flight['price'] != 'N/A' else float('inf')
                    if price <= budget * 0.6:  # Assume flights are max 60% of budget
                        filtered_flights.append(flight)
                except ValueError:
                    continue
            filtered_plan['flights'] = filtered_flights
        
        # Filter hotels by budget
        if budget and trip_plan['hotels']:
            filtered_hotels = []
            for hotel in trip_plan['hotels']:
                try:
                    price = float(hotel['price']) if hotel['price'] != 'N/A' else float('inf')
                    if price <= budget * 0.4:  # Assume hotels are max 40% of budget
                        filtered_hotels.append(hotel)
                except ValueError:
                    continue
            filtered_plan['hotels'] = filtered_hotels
        
        return filtered_plan

# Example usage
if __name__ == "__main__":
    orchestrator = TravelOrchestrator()
    
    # Plan a trip
    trip = orchestrator.plan_trip(
        origin="NYC",
        destination="PAR",
        departure_date="2023-12-25",
        return_date="2024-01-05",
        adults=2,
        budget=3000
    )
    
    print("\nTrip Plan Summary:")
    print(f"Origin: {trip['origin']}")
    print(f"Destination: {trip['destination']}")
    print(f"Dates: {trip['departure_date']} to {trip['return_date']}")
    
    print(f"\nFound {len(trip['flights'])} flight options")
    if trip['flights']:
        first_flight = trip['flights'][0]
        print(f"First flight price: {first_flight['price']} {first_flight['currency']}")
    
    print(f"\nFound {len(trip['hotels'])} hotel options")
    if trip['hotels']:
        first_hotel = trip['hotels'][0]
        print(f"First hotel: {first_hotel['name']}, Price: {first_hotel['price']}")
    
    print(f"\nWeather in {trip['destination']}: {trip['weather'].get('description', 'N/A')}")
    
    print(f"\nRecommendations:")
    for rec in trip['recommendations'][:5]:  # Show first 5 recommendations
        print(f"- {rec}")