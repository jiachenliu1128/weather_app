from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class WeatherLocation(Base):
    __tablename__ = "locations"
    # Attributes of the WeatherLocation class
    id = Column(Integer, primary_key=True, index=True)         
    city = Column(String, index=True, nullable=False)           
    country = Column(String, index=True, nullable=True)        
    lat = Column(Float, nullable=True)                        
    lon = Column(Float, nullable=True)         
    info = relationship("WeatherInfo", back_populates="location")

class WeatherInfo(Base):
    __tablename__ = "weather_info"
    # Attributes of the WeatherInfo class
    id = Column(Integer, primary_key=True, index=True)         
    location_id = Column(Integer, ForeignKey("locations.id")) 
    date = Column(Date, index=True)       
    temperature = Column(Float, nullable=False)   
    weather_description = Column(String, nullable=True)    
    # raw_data = Column(String, nullable=True)          
    location = relationship("WeatherLocation", back_populates="info")
    
    
    
    
    