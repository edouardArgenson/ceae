from db import models
from sqlalchemy.orm import Session


def get_countries_with_cities(session: Session):
    return (
        session
        .query(models.WeatherData.country, models.WeatherData.city)
        .distinct(models.WeatherData.country, models.WeatherData.city)
        .order_by(models.WeatherData.country, models.WeatherData.city)
        .all()
    )
