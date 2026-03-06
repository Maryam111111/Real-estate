import requests
from geopy.distance import geodesic


def postcode_to_coordinates(postcode):

    url = f"https://api.postcodes.io/postcodes/{postcode}"

    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()["result"]

    return data["latitude"], data["longitude"]


# simple station dataset
STATIONS = {
    "Station_A": (51.5074, -0.1278),
    "Station_B": (51.515, -0.10),
    "Station_C": (51.49, -0.08)
}


def distance_to_station(lat, lon):

    user = (lat, lon)

    distances = []

    for station in STATIONS.values():
        distances.append(geodesic(user, station).meters)

    return min(distances)