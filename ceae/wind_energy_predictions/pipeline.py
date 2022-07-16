import pandas as pd
from sqlalchemy import engine
from storage import sql_storage

from wind_energy_predictions.tasks import (
    perform_country_total_wind_energy_prediction,
    postprocess,
    preprocess,
)

PREDICTION_TABLE_NAME = "wind_energy_generation_prediction"


def run_prediction_pipeline(
    weather_data_df: pd.DataFrame, engine: engine.Engine
) -> None:
    """
    Pipeline that performs all the necessary tasks to make wind energy
    generation predictions and save them in DB.

    Args:
        weather_data_df (pd.DataFrame): OpenWeather current weather
            report as fetched from the OpenWeather API.
        engine (engine.Engine): SQLAlchemy engine that holds a
            connection to the DB.

    Returns:
        None
    """
    features_array, prediction_context = preprocess(
        weather_data_df=weather_data_df
    )

    predictions_array = perform_country_total_wind_energy_prediction(
        features_array=features_array
    )

    predictions_df = postprocess(
        predictions_array=predictions_array,
        prediction_context=prediction_context,
    )

    sql_storage.dump_append(
        df=predictions_df, sql_table_name=PREDICTION_TABLE_NAME, engine=engine
    )

    return
