from geopy import Nominatim

def get_location(place):
    location = Nominatim(user_agent="satellite_tracker").geocode(query=place)
    return location.latitude,location.longitude