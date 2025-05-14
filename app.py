from flask import Flask, render_template, request
import requests
import time
from config import API_KEY

app = Flask(__name__)

SEARCH_RADIUS = 2000
GRID_SPACING = 0.02
PLACE_TYPE_DEFAULT = "restaurant"

def get_city_coordinates(city_name):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": city_name, "key": API_KEY}
    res = requests.get(url, params=params).json()
    if res["status"] == "OK":
        location = res["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

def generate_grid(center_lat, center_lng, radius_km=10):
    delta = GRID_SPACING
    num_steps = int(radius_km / (delta * 111))
    points = []
    for dx in range(-num_steps, num_steps + 1):
        for dy in range(-num_steps, num_steps + 1):
            lat = center_lat + dy * delta
            lng = center_lng + dx * delta
            points.append((lat, lng))
    return points

def get_places(lat, lng, place_type, keyword):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": SEARCH_RADIUS,
        "type": place_type,
        "keyword": keyword,
        "key": API_KEY
    }
    all_results = []
    while True:
        res = requests.get(url, params=params).json()
        all_results.extend(res.get("results", []))
        if "next_page_token" in res:
            time.sleep(2)
            params = {"pagetoken": res["next_page_token"], "key": API_KEY}
        else:
            break
    return all_results

def check_egg(city):
    import base64
    if city.strip().lower() == "barcelona":
        return base64.b64decode("TWFsYSBzdWVydGUgQW5hIQ==").decode("utf-8")
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    easter_egg = None

    if request.method == "POST":
        city = request.form["city"]
        keyword = request.form["keyword"]
        place_type = request.form.get("type", PLACE_TYPE_DEFAULT)

        easter_egg = check_egg(city)

        lat, lng = get_city_coordinates(city)
        if lat is None:
            return render_template("index.html", error="Ciudad no encontrada", results=[], easter_egg=easter_egg)

        grid = generate_grid(lat, lng, radius_km=10)
        seen = {}

        for g_lat, g_lng in grid:
            places = get_places(g_lat, g_lng, place_type, keyword)
            for p in places:
                pid = p["place_id"]
                if pid not in seen:
                    rating = p.get("rating", 0)
                    reviews = p.get("user_ratings_total", 0)
                    # Change the weight calculation to give more importance to reviews or ratings
                    weight = 0.5 * reviews + 0.5 * rating 
                    seen[pid] = {
                        "name": p.get("name"),
                        "rating": rating,
                        "reviews": reviews,
                        "weight": weight,
                        "address": p.get("vicinity", "N/A")
                    }

        results = sorted(seen.values(), key=lambda x: x["weight"], reverse=True)[:20]

    return render_template("index.html", results=results, easter_egg=easter_egg)

if __name__ == "__main__":
    app.run(debug=True)
