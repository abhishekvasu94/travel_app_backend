import geopy
from geopy.geocoders import Nominatim

city_name = "Granada, Nicaragua"
geolocator = Nominatim(user_agent='test-2')
location = geolocator.geocode(city_name)

lat = location.latitude
long = location.longitude

print(f"Latitude: {lat}")
print(f"Longitude: {long}")
