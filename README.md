# 🌦️ Weather App Backend API

**Developed by: Jiachen Liu (刘稼晨)**

This project is a FastAPI backend featuring a SQL database for persistent storage and CRUD operations of weather data by city and date. It supports fetching and storing real-time weather information, exporting data, and is enriched with YouTube weather-related video suggestions and Google Maps integration.

**About Product Manager Accelerator:** 

Product Manager Accelerator is a global training community that empowers aspiring product managers with real-world projects, mentorship, and career coaching to accelerate their transition into product management roles.

**To activate the local FastAPI server by uvicorn:**
```bash
uvicorn app.main:app --reload
```

## 📚 API Endpoints

### 📍 Location Endpoints
- POST /locations/ – Create a new location
- GET /locations/ – List all stored locations
- DELETE /locations/{location_id} – Delete a location

**Examples:**
```bash
# Create a location
curl -X POST http://127.0.0.1:8000/locations/ \
  -H "Content-Type: application/json" \
  -d '{"city":"Toronto","country":"CA","lat":43.7,"lon":-79.4}'

# List locations
curl http://127.0.0.1:8000/locations/

# Delete a location
curl -X DELETE http://127.0.0.1:8000/locations/1
```

### 🌤️ Weather Info Endpoints
- POST /weather_infos/ – Fetch and store weather info for a location and date range
- GET /weather_infos/ – List stored weather infos
- GET /weather_infos/{info_id} – Get a specific weather info by info id
- GET /weather_infos/by_loc_date/{location_id} – Get info for a specific location and date
- GET /weather_infos/by_loc_date_range/{location_id} – Get infos by location and date range
- PUT /weather_infos/{info_id} – Update specific fields of a weather info
- DELETE /weather_infos/{info_id} – Delete weather info

**Examples:**
```bash
# Fetch & store weather info for a date range
curl -X POST http://127.0.0.1:8000/weather_infos/ \
  -H "Content-Type: application/json" \
  -d '{"city":"Toronto","country":"CA","start_date":"2025-05-14","end_date":"2025-05-16"}'

# List stored weather infos
curl http://127.0.0.1:8000/weather_infos/

# Get a specific weather info
curl http://127.0.0.1:8000/weather_infos/1

# Get info for a specific date
curl "http://127.0.0.1:8000/weather_infos/by_loc_date/1?look_up_date=2025-05-14"

# Get infos by date range
curl "http://127.0.0.1:8000/weather_infos/by_loc_date_range/1?start_date=2025-05-14&end_date=2025-05-16"

# Update a weather info
curl -X PUT http://127.0.0.1:8000/weather_infos/1 \
  -H "Content-Type: application/json" \
  -d '{"temperature":18.5}'

# Delete a weather info
curl -X DELETE http://127.0.0.1:8000/weather_infos/1
```

### 📤 Export Endpoint
- GET /export/json – Export all weather infos as JSON

**Examples:**
```bash
# Export all weather infos as JSON
curl http://127.0.0.1:8000/export/json
```

### 📹 YouTube API Endpoint
- GET /videos/{location_id} – Fetch top YouTube videos for a given location

**Examples:**
```bash
# Fetch top YouTube videos for a location
curl "http://127.0.0.1:8000/videos/1?max_results=3"
```

