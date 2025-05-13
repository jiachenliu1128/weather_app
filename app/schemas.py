from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# ----- Location Schemas -----
class LocationBase(BaseModel):
    city: str = Field(..., example="Toronto")
    country: Optional[str] = Field(None, example="CA")
    lat: Optional[float] = None
    lon: Optional[float] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True


# ----- Weather Info Request Schema -----
class WeatherInfoRequest(BaseModel):
    city: str = Field(..., example="Toronto")
    country: Optional[str] = Field(None, example="CA")
    start_date: date = Field(..., example="2025-05-01")
    end_date: date = Field(..., example="2025-05-03")


# ----- Weather Info Response Schema -----
class WeatherInfo(BaseModel):
    id: int
    location: Location
    info_date: date
    temperature: float
    description: Optional[str]
    raw_data: str

    class Config:
        orm_mode = True