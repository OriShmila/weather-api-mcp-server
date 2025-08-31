import os
from datetime import datetime, timedelta

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
    if days < 1 or days > 14:
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


async def get_historical_weather(query: str, start_date: str, end_date: str) -> dict:
    """Get historical weather data for a date range (last year)."""
    if not query:
        raise ValueError("query with location is required.")

    validate_date(start_date)
    validate_date(end_date)

    # Parse dates to validate range
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if start_dt > end_dt:
        raise ValueError("start_date must be before end_date.")

    # Check if dates are within last year
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    if start_dt < one_year_ago:
        raise ValueError("start_date cannot be more than 1 year ago.")

    if end_dt >= today:
        raise ValueError("end_date must be in the past.")

    # Collect data for each date in the range
    all_data = []
    current_date = start_dt

    while current_date <= end_dt:
        date_str = current_date.strftime("%Y-%m-%d")
        try:
            daily_data = await fetch("history.json", {"q": query, "dt": date_str})
            all_data.append(daily_data)
        except Exception:
            # Continue with other dates if one fails
            pass
        current_date += timedelta(days=1)

    if not all_data:
        raise ValueError("No historical data found for the specified date range.")

    # Return the first location info and combine all forecast days
    result = {"location": all_data[0]["location"], "forecast": {"forecastday": []}}

    for data in all_data:
        if "forecast" in data and "forecastday" in data["forecast"]:
            result["forecast"]["forecastday"].extend(data["forecast"]["forecastday"])

    return result


async def get_future_weather(query: str, date: str) -> dict:
    """Get future weather forecast for dates between 14-300 days ahead."""
    if not query:
        raise ValueError("query with location is required.")

    validate_date(date)

    # Parse the target date
    target_dt = datetime.strptime(date, "%Y-%m-%d")
    today = datetime.now()

    # Calculate days difference
    days_diff = (target_dt - today).days

    if days_diff < 14:
        raise ValueError("date must be at least 14 days in the future.")

    if days_diff > 300:
        raise ValueError("date cannot be more than 300 days in the future.")

    return await fetch("future.json", {"q": query, "dt": date})


async def get_marine_weather(query: str, with_tide: bool = False) -> dict:
    """Get marine and sailing weather forecast with optional tide data."""
    if not query:
        raise ValueError("query with location is required.")

    params = {"q": query}
    if with_tide:
        params["tide"] = "yes"

    return await fetch("marine.json", params)


TOOL_FUNCTIONS = {
    "get_weather": get_weather_forecast,
    "get_weather_history": get_weather_history,
    "get_weather_airquality": get_weather_airquality,
    "get_astronomy_data": get_astronomy_data,
    "search_locations": search_locations,
    "get_timezone": get_timezone,
    "get_sport_events": get_sport_events,
    "get_historical_weather": get_historical_weather,
    "get_future_weather": get_future_weather,
    "get_marine_weather": get_marine_weather,
}
