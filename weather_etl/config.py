import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Cities to track (you can modify this list)
CITIES = [
    "London,UK",
    "New York,US",
    "Tokyo,JP",
    "Sydney,AU",
    "Paris,FR"
]

# Database Configuration
DATABASE_URL = "sqlite:///weather_data.db"

# Data collection frequency (in minutes)
COLLECTION_INTERVAL = 30
