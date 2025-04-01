import numpy as np

def get_distance(data_json):

    cities_dist = {}
    
    for data_item in data_json:
    
        city_item_1 = data_item['city_1']
        city_item_2 = data_item['city_2']
    
        try:
            driving_dist = float(data_item['driving_leg'][0]['distance']['text'].split(" ")[0].replace(",", ""))
        except IndexError:
            driving_dist = np.inf
    
        keyname = (city_item_1, city_item_2)
    
        cities_dist[keyname] = driving_dist

    return cities_dist


def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates
