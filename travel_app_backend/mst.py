import networkx as nx
import folium
from travel_app_backend.utils import decode_polyline

def mst(data):
    
    G = nx.Graph()

    mat = []

    for k, v in data.items():
        mat.append((k[0], k[1], {"weight": v}))

    G.add_edges_from(mat)
    T = nx.minimum_spanning_tree(G)

    return T

def plot_map(T, data, mean_longitude, mean_latitude):
    locations = []

    m = folium.Map(location=(mean_latitude, mean_longitude), zoom_start=5)
    my_edges = list(T.edges)
    
    for pairs in my_edges:
    
        locations = []
    
        city_1 = pairs[0]
        city_2 = pairs[1]

        tmp = list(filter(lambda x: ((x["city_1"] == city_1) & (x["city_2"] == city_2)) | 
                          ((x["city_1"] == city_2) & (x["city_2"] == city_1)), data))
        
        try:
            for loc_data in tmp[0]['driving_leg'][0]['steps']:
                locations.extend(decode_polyline(loc_data['polyline']['points']))
        except IndexError:
            continue
            
        folium.Marker(
            location=locations[0],
            popup=folium.Popup(city_1, parse_html=True, max_width=100),
        ).add_to(m)
    
        folium.Marker(
            location=locations[-1],
            popup=folium.Popup(city_2, parse_html=True, max_width=100),
        ).add_to(m)
        folium.PolyLine(locations, tooltip="Coast").add_to(m)

    return m
