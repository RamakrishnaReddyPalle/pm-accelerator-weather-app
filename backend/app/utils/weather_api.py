# OpenWeather API integration
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from ..config import settings

OWM_BASE = "https://api.openweathermap.org/data/2.5"

class WeatherAPIError(Exception):
    pass

def _assert_key():
    if not settings.OPENWEATHER_API_KEY:
        raise WeatherAPIError("OpenWeather API key missing")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def current_weather_by_coords(lat: float, lon: float, units: str = "metric"):
    _assert_key()
    params = {"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": units}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{OWM_BASE}/weather", params=params)
        r.raise_for_status()
        data = r.json()

    return {
        "source": "openweathermap",
        "location": {
            "name": f'{data.get("name")}, {data.get("sys", {}).get("country", "")}'.strip(", "),
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
        },
        "weather": {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"].get("deg"),
            "visibility": data.get("visibility"),
            "clouds": data.get("clouds", {}).get("all"),
            "condition": data["weather"][0]["main"] if data.get("weather") else None,
            "description": data["weather"][0]["description"] if data.get("weather") else None,
            "icon": data["weather"][0]["icon"] if data.get("weather") else None,
            "sunrise": data.get("sys", {}).get("sunrise"),
            "sunset": data.get("sys", {}).get("sunset"),
            "dt": data.get("dt"),
        },
    }

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def forecast_by_coords(lat: float, lon: float, units: str = "metric", days: int = 5):
    """OpenWeather 5-day/3-hour forecast; we’ll condense to ~daily buckets."""
    _assert_key()
    params = {"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": units}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{OWM_BASE}/forecast", params=params)
        r.raise_for_status()
        data = r.json()

    loc = data.get("city", {})
    raw_list = data.get("list", [])

    # Condense to at most `days` daily summaries (pick the midday/peak timestamps if available)
    daily = []
    by_date = {}
    for item in raw_list:
        dt_txt = item.get("dt_txt")  # "YYYY-MM-DD HH:MM:SS"
        if not dt_txt:
            continue
        day = dt_txt.split(" ")[0]
        by_date.setdefault(day, []).append(item)

    for day, buckets in list(by_date.items())[:days]:
        # pick entry closest to 12:00:00 if available
        target = min(buckets, key=lambda x: abs(int(x["dt_txt"].split(" ")[1].split(":")[0]) - 12))
        daily.append({
            "date": day,
            "temp": target["main"]["temp"],
            "feels_like": target["main"]["feels_like"],
            "humidity": target["main"]["humidity"],
            "pressure": target["main"]["pressure"],
            "wind_speed": target["wind"]["speed"],
            "clouds": target.get("clouds", {}).get("all"),
            "condition": target["weather"][0]["main"] if target.get("weather") else None,
            "description": target["weather"][0]["description"] if target.get("weather") else None,
            "icon": target["weather"][0]["icon"] if target.get("weather") else None,
        })

    return {
        "source": "openweathermap",
        "location": {
            "name": f'{loc.get("name")}, {loc.get("country", "")}'.strip(", "),
            "lat": loc.get("coord", {}).get("lat"),
            "lon": loc.get("coord", {}).get("lon"),
            "timezone": loc.get("timezone"),
        },
        "forecast": daily
    }
