from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    description = Column(String)
    wind_speed = Column(Float)

    def __repr__(self):
        return f"<WeatherData(city='{self.city}', country='{self.country}', temp={self.temperature}°C)>"

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(engine)

def save_weather_data(weather_data):
    """Save weather data to the database"""
    session = Session()
    try:
        session.add(weather_data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_latest_weather():
    """Retrieve the latest weather data for each city"""
    session = Session()
    try:
        # Subquery to get the latest timestamp for each city
        latest_timestamps = session.query(
            WeatherData.city,
            WeatherData.country,
            func.max(WeatherData.timestamp).label('max_timestamp')
        ).group_by(WeatherData.city, WeatherData.country).subquery()

        # Join with the main table to get the full weather data
        results = session.query(WeatherData).join(
            latest_timestamps,
            and_(
                WeatherData.city == latest_timestamps.c.city,
                WeatherData.country == latest_timestamps.c.country,
                WeatherData.timestamp == latest_timestamps.c.max_timestamp
            )
        ).all()
        
        return results
    finally:
        session.close()
