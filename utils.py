from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="matching_app")

location_cache = {}

def normalize_location(name):
    name = name.strip()
    return name


def get_coordinates(location_name):
    if location_name in location_cache:
        return location_cache[location_name]

    try:
        location = geolocator.geocode(location_name)

        if location:
            coords = (location.latitude, location.longitude)
            location_cache[location_name] = coords
            return coords
    except:
        return None

    return None

def compute_distance_km(loc1_name, loc2_name):
    try:
        loc1 = get_coordinates(loc1_name + ", Egypt")
        loc2 = get_coordinates(loc2_name + ", Egypt")

        if loc1 is None or loc2 is None:
            return 1000  # fallback آمن

        return geodesic(loc1, loc2).km

    except:
        return 1000