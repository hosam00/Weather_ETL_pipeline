# Weather Data ETL Pipeline

This project implements a simple ETL (Extract, Transform, Load) pipeline for weather data using the OpenWeatherMap API. It collects weather data for multiple cities, stores it in a SQLite database, and provides basic data visualization.

## Features

- Collects weather data from OpenWeatherMap API
- Supports multiple cities
- Stores data in SQLite database
- Automatic data collection every 30 minutes
- Logging system for tracking operations
- Display latest weather information

## Project Structure

```
weather_etl/
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (API key)
├── config.py          # Configuration settings
├── database.py        # Database models and operations
├── weather_etl.py     # Main ETL pipeline implementation
└── weather_data.db    # SQLite database (created automatically)
```

## Setup Instructions

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)

4. Create a `.env` file in the project root and add your API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

5. Run the ETL pipeline:
   ```
   python weather_etl.py
   ```

## Configuration

You can modify the following settings in `config.py`:
- List of cities to track
- Data collection interval
- Database connection settings

## Data Model

The weather data is stored with the following fields:
- City name
- Country code
- Timestamp
- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- Weather description
- Wind speed (m/s)

## Logging

The application logs all operations to both console and `weather_etl.log` file, including:
- ETL process starts
- Data collection status for each city
- Errors and exceptions

## Contributing

Feel free to fork this project and submit pull requests with improvements!
