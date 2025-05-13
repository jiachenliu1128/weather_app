import os
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from datetime import date, datetime

# Load API key and basic variables
load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
UNITS = "metric" 




def _call_api(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call the OpenWeather API and return the weather report as a JSON dictionary.
    
    Args:
        endpoint: The API endpoint to call 
        params: A dictionary of parameters to include in the API call
        
    Returns: 
        A JSON dictionary containing the API response.
    """
    params.update({
        "appid": WEATHER_API_KEY,
        "units": UNITS,
    })
    url = f"{BASE_URL}/{endpoint}"
    resp = httpx.get(url, params=params, timeout=10.0)
    resp.raise_for_status()
    return resp.json()




def get_weather_by_city(city: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Lookup current weather by city name

    Args:
        city: The name of the city to look up
        country: Optional country code 
        
    Returns: 
        A JSON dictionary containing the current weather data.
    """
    q = f"{city},{country}" if country else city
    return _call_api("weather", {"q": q})





def get_weather_by_zip(zip: str, country: str = "us") -> Dict[str, Any]:
    """
    Lookup by postal code
    
    Args:
        zip: The postal code to look up
        country: Optional country code (default is "us")
        
    Returns:
        A JSON dictionary containing the current weather data.
    """
    return _call_api("weather", {"zip": f"{zip},{country}"})





def get_weather_by_coords(lat: float, lon: float) -> Dict[str, Any]:
    """
    Lookup by geographic coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        A JSON dictionary containing the current weather data.
    """
    return _call_api("weather", {"lat": lat, "lon": lon})





def get_forecast_by_city(city: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Lookup weather forecast by city name
    
    Args:
        city: The name of the city to look up
        country: Optional country code
        
    Returns:
        A JSON dictionary containing the weather forecast data.
    """
    q = f"{city},{country}" if country else city
    return _call_api("forecast", {"q": q})




def get_forecast_by_date_and_city(date: date, city: str, country: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Lookup weather forecast for a specific date by city name.
    
    Args:
        date: The specific date to look up (format: YYYY-MM-DD)
        city: The name of the city to look up
        country: Optional country code
        
    Returns:
        A JSON dictionary containing the weather forecast data for the specific date,
        or None if no forecast is available for that date.
    """
    forecast = get_forecast_by_city(city, country)
    for info in forecast.get("list", []):
        if info["dt_txt"].startswith(date.strftime("%Y-%m-%d")):
            return info
    return None







