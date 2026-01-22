from fastapi import FastAPI, HTTPException
from opensky import get_aircraft_by_registration, get_flight_state
from cache import last_state

app = FastAPI()

@app.get("/aircraft/{registration}")
def aircraft_lookup(registration: str):
    icao24 = get_aircraft_by_registration(registration)
    if not icao24:
        raise HTTPException(404, "Aircraft not found")
    return {"icao24": icao24}

@app.get("/flight/{icao24}")
def flight_status(icao24: str):
    current = get_flight_state(icao24)
    if not current:
        raise HTTPException(404, "Flight not active")

    alerts = []
    previous = last_state.get(icao24)

    if previous:
        if abs(current["altitude"] - previous["altitude"]) > 2000:
            alerts.append("Sudden altitude change detected")

        if abs(current["ground_speed"] - previous["ground_speed"]) > 100:
            alerts.append("Sudden speed change detected")

        if current["squawk"] != previous["squawk"]:
            alerts.append("Squawk code changed")

    last_state[icao24] = current
    return {"state": current, "alerts": alerts}
