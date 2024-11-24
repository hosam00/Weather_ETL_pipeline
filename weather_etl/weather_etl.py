import requests
import schedule
import time
from datetime import datetime
import logging
from database import WeatherData, init_db, save_weather_data, get_latest_weather
from config import API_KEY, BASE_URL, CITIES, COLLECTION_INTERVAL

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_etl.log'),
        logging.StreamHandler()
    ]
)

def extract_weather_data(city):
    """Extract weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use metric units
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {city}: {str(e)}")
        return None

def transform_weather_data(raw_data):
    """Transform raw weather data into structured format"""
    if not raw_data:
        return None

    try:
        return WeatherData(
            city=raw_data['name'],
            country=raw_data['sys']['country'],
            timestamp=datetime.utcfromtimestamp(raw_data['dt']),
            temperature=raw_data['main']['temp'],
            humidity=raw_data['main']['humidity'],
            pressure=raw_data['main']['pressure'],
            description=raw_data['weather'][0]['description'],
            wind_speed=raw_data['wind']['speed']
        )
    except KeyError as e:
        logging.error(f"Error transforming data: {str(e)}")
        return None

def etl_process():
    """Complete ETL process for all cities"""
    logging.info("Starting ETL process...")
    
    for city in CITIES:
        logging.info(f"Processing data for {city}")
        
        # Extract
        raw_data = extract_weather_data(city)
        if not raw_data:
            continue

        # Transform
        weather_data = transform_weather_data(raw_data)
        if not weather_data:
            continue

        # Load
        try:
            save_weather_data(weather_data)
            logging.info(f"Successfully saved data for {city}")
        except Exception as e:
            logging.error(f"Error saving data for {city}: {str(e)}")

def display_latest_weather():
    """Display the latest weather data for all cities"""
    latest_data = get_latest_weather()
    
    print("\nLatest Weather Data:")
    print("-" * 80)
    print(f"{'City':<15} {'Country':<8} {'Temperature':<12} {'Humidity':<10} {'Description':<20}")
    print("-" * 80)
    
    for data in latest_data:
        print(f"{data.city:<15} {data.country:<8} {data.temperature:>5.1f}°C"
              f"{data.humidity:>9}% {data.description:<20}")

def main():
    """Main function to initialize database and schedule ETL process"""
    logging.info("Initializing weather ETL pipeline...")
    
    # Initialize database
    init_db()
    
    # Schedule the ETL process
    schedule.every(COLLECTION_INTERVAL).minutes.do(etl_process)
    
    # Run ETL process immediately once
    etl_process()
    display_latest_weather()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
