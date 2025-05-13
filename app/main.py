# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import crud
from database_model import WeatherLocation, WeatherInfo
from database import Base, engine, get_db
from weather_api import get_weather_by_city, get_forecast_by_date_and_city

# Initialize the database and api
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Weather APP Backend API")




################################################################################
# WeatherLocation API Endpoints
################################################################################
@app.post("/locations/", summary="Create a new location")
def create_location(location: dict, db: Session = Depends(get_db)) -> WeatherLocation:
    """
    Create a new location in the database.

    Args:
        location (dict): A dictionary containing location data. Expected keys are:
            - city: The name of the city
            - country: The country code (optional)
            - lat: Latitude (optional)
            - lon: Longitude (optional)
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Returns:
        WeatherLocation: The created WeatherLocation object.
    """
    city = location.get("city")
    country = location.get("country")
    lat = location.get("lat")
    lon = location.get("lon")
    db_loc = crud.create_location(db, city=city, country=country, lat=lat, lon=lon)
    return db_loc




@app.get("/locations/", summary="List locations")
def list_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[WeatherLocation]:
    """
    List all stored locations with pagination.

    Args:
        skip (int, optional): How many records to skip. Defaults to 0.
        limit (int, optional): How many records to return. Defaults to 100.
        db (Session, optional): A database session. Defaults to Depends(get_db).
        
    Returns:
        List[WeatherLocation]: A list of WeatherLocation objects.
    """
    return crud.list_locations(db, skip=skip, limit=limit)





@app.delete("/locations/{loc_id}", summary="Delete a location")
def delete_location(loc_id: int, db: Session = Depends(get_db)) -> WeatherLocation:
    """
    Delete a location by its ID.

    Args:
        loc_id (int): The ID of the location to delete.
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the location is not found, a 404 error is raised.

    Returns:
        WeatherLocation: The deleted WeatherLocation object.
    """
    loc = crud.delete_location(db, loc_id)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc




################################################################################
# WeatherInfo API Endpoints
################################################################################
@app.post("/weather_infos/", summary="Fetch and store weather info for a location and date range")
def create_info(input: dict, db: Session = Depends(get_db)) -> list[WeatherInfo]:
    """
    Fetch and store weather information for a given location and date range.

    Args:
        input (dict): A dictionary containing the following
            - city: The name of the city
            - country: The country code (optional)
            - start_date: The start date for the weather info (expected format: YYYY-MM-DD)
            - end_date: The end date for the weather info (expected format: YYYY-MM-DD)
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the input is invalid or if the location is not found, a 400 error is raised.

    Returns:
        WeatherInfo: The created WeatherInfo object.
    """
    # Validate input
    city = input.get("city")
    country = input.get("country")
    start_date = input.get("start_date")  
    end_date = input.get("end_date") 
    
    # Check if required input are present
    if not city or not start_date or not end_date:
        raise HTTPException(status_code=400, detail="city, start_date, and end_date are required")
    
    # Validate date format and range
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    if start > end:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    # NOTE: The API does not support historical data, so we will only fetch 
    # current weather till the date range is supported.
    if start < date.today() or end < date.today():
        raise HTTPException(status_code=400, detail="Historical data is not supported in free OpenWeather API")
    # Check if the date range is more than 5 days in the future
    if (start > date.today() + date.timedelta(days=5) or 
        end > date.today() + date.timedelta(days=5)):
        raise HTTPException(status_code=400, detail="Max 5 days forecast supported in free OpenWeather API")
    
    # Get or create location
    loc = crud.get_location_by_city(db, city, country)
    if not loc:
        data = get_weather_by_city(city, country)
        loc = crud.create_location(db, city=city, country=country,
                                   lat=data["coord"]["lat"], lon=data["coord"]["lon"])
    
    # For each date in range, fetch weather data and store it
    infos = []
    current = start
    while current <= end:
        # Check if the weather info for the current date already exists
        info = crud.get_info_by_loc_date(db, location_id=loc.id, date=current)
        if not info:
            # Info for current date does not exist, fetch weather data for the current date
            if current == date.today():
                info_data = get_weather_by_city(city, country)
            else:
                info_data = get_forecast_by_date_and_city(city, country)
            # Store the weather info in the database
            temp = info_data["main"]["temp"]
            desc = info_data["weather"][0]["description"]
            raw = str(info_data)
            info = crud.create_info(
                db,
                location_id=loc.id,
                info_date=current,
                temperature=temp,
                description=desc,
                raw_data=raw
            )
        infos.append(info)
        current += date.timedelta(days=1)
    return infos
    



@app.get("/weather_infos/", summary="List stored weather infos")
def list_infos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[WeatherInfo]:
    """
    List all stored weather information with pagination.

    Args:
        skip (int, optional): item to skip for pagination. Defaults to 0.
        limit (int, optional): maximum number of items to return. Defaults to 100.
        db (Session, optional): A database session. Defaults to Depends(get_db).
        
    Returns:
        List[WeatherInfo]: A list of WeatherInfo objects.
    """
    return crud.list_infos(db, skip=skip, limit=limit)





@app.get("/weather_infos/{info_id}", summary="Get a specific weather info")
def get_info(info_id: int, db: Session = Depends(get_db)) -> WeatherInfo:
    """
    Get a specific weather info by its ID.

    Args:
        info_id (int): The ID of the weather info to retrieve.
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the weather info is not found, a 404 error is raised.

    Returns:
        WeatherInfo: The requested WeatherInfo object.
    """
    info = crud.get_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Weather info not found")
    return info




@app.put("/weather_infos/{info_id}", summary="Update weather info fields")
def update_info(info_id: int, updates: dict, db: Session = Depends(get_db)) -> WeatherInfo:
    """
    Update specific fields of a weather info.

    Args:
        info_id (int): The ID of the weather info to update.
        updates (dict): A dictionary containing the fields to update. Expected keys are:
            - temperature: The new temperature value
            - weather_description: The new weather description
            - raw_data: The new raw data string
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the weather info is not found, a 404 error is raised.

    Returns:
        WeatherInfo: The updated WeatherInfo object.
    """
    info = crud.update_info(db, info_id, updates)
    if not info:
        raise HTTPException(status_code=404, detail="Weather info not found")
    return info




@app.delete("/weather_infos/{info_id}", summary="Delete weather info")
def delete_weather_info(info_id: int, db: Session = Depends(get_db)) -> WeatherInfo:
    """
    Delete a weather info by its ID.

    Args:
        info_id (int): The ID of the weather info to delete.
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the weather info is not found, a 404 error is raised.

    Returns:
        WeatherInfo: The deleted WeatherInfo object.
    """
    info = crud.delete_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Weather info not found")
    return info




@app.get("/weather_infos/by_loc_date/{loc_id}", summary="Get infos by location and specific date")
def get_info_by_loc_date(loc_id: int, date_str: str, db: Session = Depends(get_db)) -> WeatherInfo:
    """
    Retrieve weather information for a specific location and date.

    Args:
        loc_id (int): The ID of the location.
        date_str (str): The date to retrieve info for (format: YYYY-MM-DD).
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Returns:
        WeatherInfo: The WeatherInfo object for the specified location and date.
    """
    info_date = date.fromisoformat(date_str)
    info = crud.get_info_by_loc_date(db, loc_id, info_date)
    if not info:
        raise HTTPException(status_code=404, detail="Weather info not found")
    return info




@app.get("/weather_infos/by_loc_date_range/{loc_id}", summary="Get infos by location and date range")
def get_infos_by_loc_date_range(loc_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)) -> list[WeatherInfo]:
    """
    Retrieve weather information for a specific location and date range.

    Args:
        loc_id (int): The ID of the location.
        start_date (str): The start date for the range (format: YYYY-MM-DD).
        end_date (str): The end date for the range (format: YYYY-MM-DD).
        db (Session, optional): A database session. Defaults to Depends(get_db).

    Returns:
        List[WeatherInfo]: A list of WeatherInfo objects for the specified location and date range.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    infos = crud.get_infos_by_loc_date_range(db, loc_id, start, end)
    return infos






