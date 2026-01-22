import requests
from requests.auth import HTTPBasicAuth

OPENSKY_URL = "https://opensky-network.org/api"

USERNAME = "YOUR_OPENSKY_USERNAME"
PASSWORD = "YOUR_OPENSKY_PASSWORD"

auth = HTTPBasicAuth(USERNAME, PASSWORD)

def get_aircraft_by_registration(reg):
    r = requests.get(f"{OPENSKY_URL}/metadata/aircraft/list", auth=auth)
    r.raise_for_status()
    for ac in r.json():
        if ac.get("registration", "").upper() == reg.upper():
            return ac.get("icao24")
    return None

def get_flight_state(icao24):
    r = requests.get(f"{OPENSKY_URL}/states/all?icao24={icao24}", auth=auth)
    r.raise_for_status()
    states = r.json().get("states")
    if not states:
        return None

    s = states[0]
    return {
        "on_ground": s[8],
        "latitude": s[6],
        "longitude": s[5],
        "altitude": s[7],
        "ground_speed": s[9],
        "vertical_rate": s[11],
        "squawk": s[14]
    }
