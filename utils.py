from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="matching_app")

location_cache = {}

def normalize_location(name):
    name = name.strip()
    return name

def get_coordinates(location_name):
    try:
        location_name = normalize_location(location_name)

        if location_name in location_cache:
            return location_cache[location_name]

        location = geolocator.geocode(location_name + ", Egypt")

        if location:
            coords = (location.latitude, location.longitude)
            location_cache[location_name] = coords
            return coords

        return None
    except:
        return None


def compute_distance_km(row, donor):
    try:
        loc1 = get_coordinates(row["location_requester"])
        loc2 = get_coordinates(donor["location"])

        if loc1 is None or loc2 is None:
            return 9999

        return geodesic(loc1, loc2).km
    except:
        return 9999