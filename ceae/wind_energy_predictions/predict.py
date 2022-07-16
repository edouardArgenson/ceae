import datetime as dt
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

PRODUCTION_MODEL_PATH = (
    "/ceae/ceae/wind_energy_predictions/models/simple_regression.joblib"
)


def _load_model(model_path: str) -> BaseEstimator:
    return joblib.load(model_path)


def _build_prediction_df(
    country: str, time: dt.datetime, timezone: int, prediction: float
) -> pd.DataFrame:
    data = {
        "country": [country],
        "datetime": [time],
        "timezone": [timezone],
        "prediction": [prediction],
    }
    return pd.DataFrame(data)


def preprocess(
    weather_data_df: pd.DataFrame
) -> Tuple[np.array, str, dt.datetime, int]:
    country_to_predict = "FR"
    reference_city = "Arrondissement de Vannes"

    indexed_weather_data_df = weather_data_df.set_index(
        ["city", "country", "datetime"]
    )

    ref_city_data = indexed_weather_data_df.loc[
        (reference_city, country_to_predict, slice(None)), :
    ]

    # We should have one and only one row per query for
    # ref_city_data.
    if len(ref_city_data) == 0:
        raise ValueError(
            "Could not find necessary `wind_speed` data from fetched "
            "weather data"
        )

    if len(ref_city_data) > 1:
        raise ValueError(
            "Found too many `wind_speed` data from fetched weather data. "
            "Maybe some identical data is fetched several times."
        )

    # The only feature is the `wind_speed` column.
    features_array = ref_city_data.loc[:, ["wind_speed"]].to_numpy()

    time = ref_city_data.iloc[0].loc["datetime"]
    timezone = ref_city_data.iloc[0].loc["timezone"]

    return features_array, country_to_predict, time, timezone


def perform_country_total_wind_energy_prediction(
    features_array: np.array
) -> np.array:
    """Load model and preform predictions."""
    model = _load_model(PRODUCTION_MODEL_PATH)
    return model.predict(features_array)


def postprocess(
    predictions_array: np.array,
    country: str,
    time: dt.datetime,
    timezone: int,
) -> pd.DataFrame:
    if len(predictions_array) != 1:
        raise ValueError(
            "Postprocessing implemented for only one prediction at a time"
        )
    
    prediction = predictions_array[0]

    return _build_prediction_df(
        country=country, time=time, timezone=timezone, prediction=prediction
    )
