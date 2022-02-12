from sqlalchemy import CheckConstraint, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import (
    FLOAT, INTEGER, NUMERIC, SMALLINT, TIMESTAMP, VARCHAR
)


# declarative base class
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = "weather_data"

    city = Column(VARCHAR(length=32), primary_key=True)
    country = Column(VARCHAR(length=32), primary_key=True)
    datetime = Column(TIMESTAMP(timezone=False), primary_key=True)
    
    main = Column(VARCHAR(length=32), nullable=False)
    description = Column(VARCHAR(length=32), nullable=False)
    temperature = Column(FLOAT, nullable=False)
    wind_speed = Column(FLOAT, CheckConstraint("wind_speed >= 0"), nullable=False)
    wind_dir = Column(SMALLINT, CheckConstraint("wind_dir >= 0 AND wind_dir <= 360"), nullable=False)
    humidity = Column(SMALLINT, CheckConstraint("humidity >= 0 AND humidity <= 100"), nullable=False)
    rain_1h = Column(NUMERIC(precision=4, scale=2), CheckConstraint("rain_1h >= 0"), nullable=False)
    rain_3h = Column(NUMERIC(precision=4, scale=2), CheckConstraint("rain_3h >= 0"), nullable=False)
    clouds = Column(SMALLINT, CheckConstraint("clouds >= 0 AND clouds <= 100"), nullable=False)
    visibility = Column(INTEGER, CheckConstraint("visibility >= 0"), nullable=False)
    timezone = Column(INTEGER, nullable=False)
