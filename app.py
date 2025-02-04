import openrouteservice
from openrouteservice import convert
import folium
from folium import GeoJson

# Initialize the client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf62484051ea57a35a442c9a50c4a8be0c9cff')

# Define coordinates (latitude, longitude)
start_coords = (77.5385, 8.0883)  # Los Angeles (Longitude, Latitude)
end_coords = (74.7973, 34.0836)       # Los Angeles

try:
    # Get the route between two points
    route = client.directions(
        coordinates=[start_coords, end_coords],
        profile='driving-car',  # for car driving
        format='geojson'
    )
    
    # Extract distance and duration
    distance = route['features'][0]['properties']['segments'][0]['distance']  # in meters
    duration = route['features'][0]['properties']['segments'][0]['duration']/(60*60) # in seconds
    
    print(f"Distance: {distance} meters")
    print(f"Duration: {duration} hours")

    map_center = [start_coords[1], start_coords[0]]  # [lat, lon]
    m = folium.Map(location=map_center, zoom_start=6)

    # Add route to map using GeoJSON
    folium.GeoJson(route).add_to(m)

    # Add a marker for the start and end locations
    folium.Marker(location=[start_coords[1], start_coords[0]], popup='Start').add_to(m)
    folium.Marker(location=[end_coords[1], end_coords[0]], popup='End').add_to(m)

    # Save the map as an HTML file
    m.save("route_map.html")
    print("Map has been saved as 'route_map.html'")

except Exception as e:
    print(f"An error occurred: {e}")
