from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from .database_model import WeatherLocation, WeatherInfo

################################################################################
# WeatherLocation CRUD operations
################################################################################
def create_location(
    db: Session,
    city: str,
    country: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None
) -> WeatherLocation:
    """
    Create a new WeatherLocation record.
    
    Args:
        db: Database session
        city: The name of the city
        country: Optional country code
        lat: Optional latitude
        lon: Optional longitude
        
    Returns:
        A WeatherLocation database object.
    """
    db_loc = WeatherLocation(city=city, country=country, lat=lat, lon=lon)
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc


def get_location_by_city(db: Session, city: str, country: Optional[str] = None) -> Optional[WeatherLocation]:
    """
    Retrieve a location by city (and optional country code).
    
    Args:
        db: Database session
        city: The name of the city to look up
        country: Optional country code
        
    Returns:   
        A WeatherLocation database object if found, otherwise None.
    """
    query = db.query(WeatherLocation).filter(WeatherLocation.city == city)
    if country:
        query = query.filter(WeatherLocation.country == country)
    return query.first()


def list_locations(db: Session, skip: int = 0, limit: int = -1) -> List[WeatherLocation]:
    """
    List stored locations with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return. If -1, return all records.  
    
    Returns:
        A list of WeatherLocation database objects.
    """
    if limit < -1:
        raise ValueError("The 'limit' parameter must be -1 or a non-negative integer.")
    if limit == -1:
        return db.query(WeatherLocation).offset(skip).all()
    return db.query(WeatherLocation).offset(skip).limit(limit).all()


def delete_location(db: Session, loc_id: int) -> Optional[WeatherLocation]:
    """
    Delete a location and its info.
    
    Args:
        db: Database session
        loc_id: ID of the location to delete
        
    Returns:
        A WeatherLocation database object if deleted, otherwise None.
    """
    loc = db.query(WeatherLocation).get(loc_id)
    if not loc:
        return None
    db.delete(loc)
    db.commit()
    return loc




################################################################################
# WeatherInfo CRUD operations
################################################################################
def create_info(
    db: Session,
    location_id: int,
    info_date: date,
    temperature: float,
    weather_description: str,
    # raw_data: str
) -> WeatherInfo:
    """
    Create a new weather info linked to a location.
    
    Args:
        db: Database session
        location_id: ID of the location
        info_date: Date of the weather info
        temperature: Temperature value
        weather_description: Weather description
        raw_data: Raw data string
        
    Returns:    
        A WeatherInfo database object.
    """
    # get the location to ensure it exists
    location = db.query(WeatherLocation).get(location_id)
    if not location:
        raise ValueError(f"Location with ID {location_id} does not exist.")
    db_info = WeatherInfo(
        location_id=location_id,
        date=info_date,
        temperature=temperature,
        weather_description=weather_description,
        # raw_data=raw_data,
        location=location
    )
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info


def get_info(db: Session, info_id: int) -> Optional[WeatherInfo]:
    """
    Retrieve a single weather info by ID.
    
    Args:
        db: Database session
        info_id: ID of the weather info to retrieve
    
    Returns:
        A WeatherInfo database object if found, otherwise None.
    """
    return db.query(WeatherInfo).filter(WeatherInfo.id == info_id).first()


def list_infos(
    db: Session,
    skip: int = 0,
    limit: int = -1
) -> List[WeatherInfo]:
    """
    List all weather info with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip 
        limit: Maximum number of records to return. If -1, return all records.
        
    Returns:
        A list of WeatherInfo database objects.
    """
    if limit < -1:
        raise ValueError("The 'limit' parameter must be -1 or a non-negative integer.")
    if limit == -1:
        return db.query(WeatherInfo).offset(skip).all()
    return db.query(WeatherInfo).offset(skip).limit(limit).all()


def get_info_by_loc_date(
    db: Session,
    location_id: int,
    date: date,
) -> List[WeatherInfo]:
    """
    Retrieve info for a location of a date.
    
    Args:
        db: Database session
        location_id: ID of the location
        date: Date to look up
        
    Returns:  
        A list of WeatherInfo database objects. 
    """
    return (
        db.query(WeatherInfo)
        .filter(
            WeatherInfo.location_id == location_id,
            WeatherInfo.date == date
        )
        .first()
    )


def get_infos_by_loc_date_range(
    db: Session,
    location_id: int,
    start_date: date,
    end_date: date
) -> List[WeatherInfo]:
    """
    Retrieve info for a location within a date range.
    
    Args:
        db: Database session
        location_id: ID of the location
        start_date: Start date for the range
        end_date: End date for the range
        
    Returns:  
        A list of WeatherInfo database objects. 
    """
    return (
        db.query(WeatherInfo)
        .filter(
            WeatherInfo.location_id == location_id,
            WeatherInfo.date.between(start_date, end_date)
        )
        .all()
    )


def update_info(
    db: Session,
    info_id: int,
    updates: Dict[str, Any]
) -> Optional[WeatherInfo]:
    """
    Update fields of an existing weather info.
    
    Args:
        db: Database session
        info_id: ID of the weather info to update
        updates: Dictionary of fields to update with their new values
        
    Returns:
        A WeatherInfo database object if updated, otherwise None.   
    """
    info = get_info(db, info_id)
    if not info:
        return None
    for field, value in updates.items():
        if hasattr(info, field):
            setattr(info, field, value)
    db.commit()
    db.refresh(info)
    return info


def delete_info(db: Session, info_id: int) -> Optional[WeatherInfo]:
    """
    Delete a weather info by ID.
    
    Args:
        db: Database session
        info_id: ID of the weather info to delete
        
    Returns:
        A WeatherInfo database object if deleted, otherwise None.
    """
    info = get_info(db, info_id)
    if not info:
        return None
    db.delete(info)
    db.commit()
    return info



