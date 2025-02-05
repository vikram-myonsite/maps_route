import openrouteservice
import folium
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load OpenRouteService API key from environment variable
openroute_api_key = "5b3ce3597851110001cf62484051ea57a35a442c9a50c4a8be0c9cff"
client = openrouteservice.Client(key=openroute_api_key)
# Route to get distance, duration, and map based on input coordinates (GET method)
@app.route('/', methods=['GET'])
def get_route():
    try:
        # Get lat/lon from query parameters
        start_lat = request.args.get("start_lat", type=float)
        start_lon = request.args.get("start_lon", type=float)
        end_lat = request.args.get("end_lat", type=float)
        end_lon = request.args.get("end_lon", type=float)

        if None in [start_lat, start_lon, end_lat, end_lon]:
            return jsonify({"error": "Missing latitude or longitude parameters"}), 400

        # Define coordinates for OpenRouteService
        start_coords = (start_lon, start_lat)  # OpenRouteService requires (longitude, latitude)
        end_coords = (end_lon, end_lat)

        # Fetch route from OpenRouteService
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile="driving-car",
            format="geojson"
        )

        # Extract distance & duration
        distance = route["features"][0]["properties"]["segments"][0]["distance"] / 1000  # Convert meters to km
        duration = route["features"][0]["properties"]["segments"][0]["duration"] / 3600  # Convert seconds to hours

        # Generate Folium map
        map_center = [start_lat, start_lon]
        m = folium.Map(location=map_center, zoom_start=6)
        folium.GeoJson(route).add_to(m)
        folium.Marker([start_lat, start_lon], popup="Start").add_to(m)
        folium.Marker([end_lat, end_lon], popup="End").add_to(m)
        
        # Save map as an HTML file
        map_filename = "route_map.html"
        m.save(map_filename)

        # Return JSON response
        return jsonify({
            "distance_km": round(distance, 2),
            "duration_hours": round(duration, 2),
            "map_url": f"https://your-api.onrender.com/{map_filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle POST request with JSON data (POST method)
@app.route('/', methods=['POST'])
def post_route():
    try:
        # Get JSON data from POST request
        data = request.get_json()

        start_lat = data.get("start_lat")
        start_lon = data.get("start_lon")
        end_lat = data.get("end_lat")
        end_lon = data.get("end_lon")

        if None in [start_lat, start_lon, end_lat, end_lon]:
            return jsonify({"error": "Missing latitude or longitude in JSON"}), 400

        # Define coordinates for OpenRouteService
        start_coords = (start_lon, start_lat)  # OpenRouteService requires (longitude, latitude)
        end_coords = (end_lon, end_lat)

        # Fetch route from OpenRouteService
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile="driving-car",
            format="geojson"
        )

        # Extract distance & duration
        distance = route["features"][0]["properties"]["segments"][0]["distance"] / 1000  # Convert meters to km
        duration = route["features"][0]["properties"]["segments"][0]["duration"] / 3600  # Convert seconds to hours

        # Generate Folium map
        map_center = [start_lat, start_lon]
        m = folium.Map(location=map_center, zoom_start=6)
        folium.GeoJson(route).add_to(m)
        folium.Marker([start_lat, start_lon], popup="Start").add_to(m)
        folium.Marker([end_lat, end_lon], popup="End").add_to(m)
        
        # Save map as an HTML file
        map_filename = "route_map.html"
        m.save(map_filename)

        # Return JSON response
        return jsonify({
            "distance_km": round(distance, 2),
            "duration_hours": round(duration, 2),
            "map_url": f"https://your-api.onrender.com/{map_filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
