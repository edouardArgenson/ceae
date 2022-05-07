from db import models
from sqlalchemy.orm import Session


def get_city(country_code: str, city_name, session: Session):
    return (
        session
        .query(models.WeatherData.city)
        .filter(
            models.WeatherData.country == country_code,
            models.WeatherData.city == city_name,
        )
        .distinct(models.WeatherData.country, models.WeatherData.city)
        .all()
    )


def get_countries_with_cities(session: Session):
    return (
        session
        .query(models.WeatherData.country, models.WeatherData.city)
        .distinct(models.WeatherData.country, models.WeatherData.city)
        .order_by(models.WeatherData.country, models.WeatherData.city)
        .all()
    )


def get_country_with_cities(country_code: str, session: Session):
    return (
        session
        .query(models.WeatherData.city)
        .filter(models.WeatherData.country == country_code)
        .distinct(models.WeatherData.country, models.WeatherData.city)
        .order_by(models.WeatherData.city)
        .all()
    )


def get_weather(country_code: str, city_name: str, session: Session):
    return (
        session
        .query(
            models.WeatherData.datetime,
            models.WeatherData.timezone,
            models.WeatherData.main,
            models.WeatherData.description,
            models.WeatherData.temperature,
            models.WeatherData.wind_speed,
            models.WeatherData.wind_dir,
            models.WeatherData.humidity,
            models.WeatherData.rain_1h,
            models.WeatherData.rain_3h,
            models.WeatherData.clouds,
            models.WeatherData.visibility,
        )
        .filter(
            models.WeatherData.country == country_code,
            models.WeatherData.city == city_name,
        )
        .order_by(models.WeatherData.datetime)
        .all()
    )
