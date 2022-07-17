import datetime
import os
import sys

from db.helpers import build_database_uri
from sqlalchemy import create_engine

from data_fetchers.current_weather import (
    run_fetch_cities_current_weather_pipeline
)
from wind_energy_predictions.pipeline import run_prediction_pipeline


def run_pipeline() -> bool:
    # config.
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    REQUEST_CONFIG_PATH = "config/openweather_cities.yml"

    database_uri = build_database_uri(
        dialect=os.environ.get("CEAE_DB_DIALECT"),
        user=os.environ.get("CEAE_DB_USER"),
        password=os.environ.get("CEAE_DB_PASSWORD"),
        host=os.environ.get("CEAE_DB_HOST"),
        dbname=os.environ.get("CEAE_DB_NAME"),
    )
    SQL_ENGINE = create_engine(database_uri, echo=True)

    print("--------------")
    print(f"Launching pipeline (now='{datetime.datetime.now()}').")

    weather_df = run_fetch_cities_current_weather_pipeline(
        request_config_path=REQUEST_CONFIG_PATH,
        api_key=OPENWEATHER_API_KEY,
        engine=SQL_ENGINE,
    )

    run_prediction_pipeline(weather_data_df=weather_df, engine=SQL_ENGINE)

    return True


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(int(not success))
