import datetime as dt
from typing import Optional

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


def get_weather(
    country_code: str,
    city_name: str,
    start_date: Optional[dt.datetime],
    end_date: Optional[dt.datetime],
    session: Session,
):
    criterions = [
        models.WeatherData.country == country_code,
        models.WeatherData.city == city_name,
    ]

    if start_date:
        criterions.append(models.WeatherData.datetime >= start_date)
    if end_date:
        criterions.append(models.WeatherData.datetime < end_date)

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
        .filter(*criterions)
        .order_by(models.WeatherData.datetime)
        .all()
    )


def get_wind_energy_generation_predictions(
    start_date: Optional[dt.datetime],
    end_date: Optional[dt.datetime],
    session: Session,
):
    criterions = []

    if start_date:
        criterions.append(
            models.WindEnergyGenerationPrediction.datetime >= start_date
        )
    if end_date:
        criterions.append(
            models.WindEnergyGenerationPrediction.datetime < end_date
        )

    return (
        session
        .query(
            models.WindEnergyGenerationPrediction.country,
            models.WindEnergyGenerationPrediction.datetime,
            models.WindEnergyGenerationPrediction.timezone,
            models.WindEnergyGenerationPrediction.prediction,
            models.WindEnergyGenerationPrediction.unit,
        )
        .filter(*criterions)
        .order_by(
            models.WindEnergyGenerationPrediction.country,
            models.WindEnergyGenerationPrediction.datetime,
        )
        .all()
    )
