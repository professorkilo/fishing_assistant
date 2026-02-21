import httpx
from timezonefinder import TimezoneFinder
from homeassistant.core import HomeAssistant

def resolve_location_metadata_sync(lat: float, lon: float) -> dict:
    """Calculate timezone and elevation for a given lat/lon (sync-safe)."""
    from homeassistant.util import dt as dt_util

    tf = TimezoneFinder()
    timezone = (
        tf.certain_timezone_at(lat=lat, lng=lon)
        or tf.timezone_at(lat=lat, lng=lon)
        or tf.closest_timezone_at(lat=lat, lng=lon)
        or str(dt_util.DEFAULT_TIME_ZONE)
    )
    elevation = 500

    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            result = response.json().get("results", [{}])[0]
            elevation = result.get("elevation", elevation)
    except Exception:
        pass  # Fail silently for now

    return {
        "timezone": timezone,
        "elevation": elevation
    }
