import os
from datetime import datetime

import httpx
from dotenv import load_dotenv


load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def validate_date(dt_str: str) -> None:
    try:
        datetime.strptime(dt_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date: {dt_str}. Use YYYY-MM-DD.")


async def fetch(endpoint: str, params: dict) -> dict:
    if not WEATHER_API_KEY:
        raise ValueError("Weather API key not set.")

    params["key"] = WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/{endpoint}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params)
            try:
                data = resp.json()
            except Exception:
                data = None
            if resp.status_code != 200:
                detail = (data or {}).get("error", {}).get("message", resp.text)
                raise ValueError(f"WeatherAPI error: {detail}")
            return data
        except httpx.RequestError as e:
            raise ValueError(f"Request error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")


async def get_current_weather(query: str, include_air_quality: bool = False) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    return await fetch(
        "current.json", {"q": query, "aqi": "yes" if include_air_quality else "no"}
    )


async def get_weather_forecast(
    query: str,
    days: int = 1,
    include_air_quality: bool = False,
    include_alerts: bool = False,
) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    # Free plan only allows 3 days of forecast
    if days < 1 or days > 3:
        raise ValueError("'days' must be between 1 and 3.")
    return await fetch(
        "forecast.json",
        {
            "q": query,
            "days": days,
            "aqi": "yes" if include_air_quality else "no",
            "alerts": "yes" if include_alerts else "no",
        },
    )


async def get_weather_history(query: str, date: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    validate_date(date)
    return await fetch("history.json", {"q": query, "dt": date})


async def get_weather_airquality(query: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    return await fetch("current.json", {"q": query, "aqi": "yes"})


async def get_astronomy_data(query: str, date: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    validate_date(date)
    return await fetch("astronomy.json", {"q": query, "dt": date})


async def search_locations(query: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    locations = await fetch("search.json", {"q": query})
    return {"items": locations}


async def get_timezone(query: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    return await fetch("timezone.json", {"q": query})


async def get_sport_events(query: str) -> dict:
    if not query:
        raise ValueError("query with location is required.")
    return await fetch("sports.json", {"q": query})


TOOL_FUNCTIONS = {
    "get_weather": get_weather_forecast,
    "get_weather_history": get_weather_history,
    "get_weather_airquality": get_weather_airquality,
    "get_astronomy_data": get_astronomy_data,
    "search_locations": search_locations,
    "get_timezone": get_timezone,
    "get_sport_events": get_sport_events,
}
