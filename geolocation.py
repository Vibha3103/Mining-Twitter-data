import json
import folium
from geopy.geocoders import Nominatim
import time

fname = 'tweets.json'


geo_data = {"type": "FeatureCollection", "features": []}

# Optional geocoder for text locations (if exact GPS coordinates are missing)
geolocator = Nominatim(user_agent="covid_twitter_mining_app")
location_cache = {}
geocode_limit = 30  # Limit geocoding calls so the script runs fast
geocoded_count = 0

with open(fname, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        tweet = json.loads(line)
        text = tweet.get('text') or tweet.get('original_text', 'No text')
        created_at = tweet.get('created_at', '')

        # Case A: Standard Twitter GeoJSON coordinates [longitude, latitude]
        if tweet.get('coordinates'):
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": text,
                    "created_at": created_at
                }
            }
            geo_data['features'].append(geo_json_feature)

        # Case B: Fallback if CSV only had a 'location' or 'place' string
        elif geocoded_count < geocode_limit:
            loc_str = tweet.get('location') or tweet.get('place') or tweet.get('user_location')
            if isinstance(loc_str, dict):
                loc_str = loc_str.get('full_name')
            
            if loc_str and isinstance(loc_str, str):
                loc_clean = loc_str.strip()
                if loc_clean not in location_cache:
                    try:
                        loc = geolocator.geocode(loc_clean, timeout=5)
                        time.sleep(1)  # Respect Nominatim rate limit (1 req/sec)
                        location_cache[loc_clean] = (loc.longitude, loc.latitude) if loc else None
                        geocoded_count += 1
                    except Exception:
                        location_cache[loc_clean] = None

                coords = location_cache.get(loc_clean)
                if coords:
                    geo_json_feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [coords[0], coords[1]]
                        },
                        "properties": {
                            "text": f"[{loc_clean}] {text}",
                            "created_at": created_at
                        }
                    }
                    geo_data['features'].append(geo_json_feature)

# 2. Save GeoJSON file (matches Part 7 of Marco Bonzanini's tutorial)
with open('geo_data.json', 'w', encoding='utf-8') as fout:
    fout.write(json.dumps(geo_data, indent=4))

print(f"Total geolocated tweets found: {len(geo_data['features'])}")

# 3. Build the Interactive Map with Folium (Python wrapper for Leaflet.js)
# Centered globally at [20, 0] with zoom level 2
tweet_map = folium.Map(location=[20, 0], zoom_start=2, tiles='OpenStreetMap')

# Add each tweet as an interactive marker with a popup
for feature in geo_data['features']:
    lon, lat = feature['geometry']['coordinates']
    popup_text = f"<b>{feature['properties']['created_at']}</b><br>{feature['properties']['text']}"
    
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(tweet_map)

# Save the map to an HTML file
output_html = 'covid_tweets_map.html'
tweet_map.save(output_html)
print(f"Map saved! Open '{output_html}' in your browser to view the interactive map.")
