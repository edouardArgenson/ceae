import datetime as dt
from typing import NamedTuple, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

PRODUCTION_MODEL_PATH = (
    "/ceae/ceae/wind_energy_predictions/models/simple_regression.joblib"
)
PREDICTION_UNIT = "MW"


class PredictionContext(NamedTuple):
    """
    Container class for prediction context data.

    Attributes:
        country (str): Code of the country for which we are predicting
            the total wind energy generation (for instance: `FR`).
        time (dt.datetime):  Datetime of the prediction.
        timezone (int):  Shift in seconds from UTC.
    """
    country: str
    time: dt.datetime
    timezone: int


def _load_model(model_path: str) -> BaseEstimator:
    """
    Helper that loads and deserializes a scikit-learn model using
    joblib.
    """
    return joblib.load(model_path)


def _build_prediction_df(
    prediction_context: PredictionContext,
    prediction: float,
    unit: str,
) -> pd.DataFrame:
    """
    Formats predictions following the DB table on which predictions are
    to be inserted structure.
    """
    data = {
        "country": [prediction_context.country],
        "datetime": [prediction_context.time],
        "timezone": [prediction_context.timezone],
        "prediction": [prediction],
        "unit": [unit],
    }
    return pd.DataFrame(data)


def preprocess(
    weather_data_df: pd.DataFrame
) -> Tuple[np.array, PredictionContext]:
    """
    Extracts and formats weather data from the full OpenWeather current
    weather data report, as a numpy array ready to be used by the model
    to perform predictions.

    As now, the model uses data from only one city, the `reference_city`.
    The only weather data used is the `wind_speed`.

    We perform predictions for one point at a time, so the return array
    contains only one row.

    Args:
        weather_data_df (pd.DataFrame): OpenWeather current weather
            report as fetched from the OpenWeather API.

    Returns:
        np.array: Formatted features array ready to be used by the
            model to perform predictions.
        PredictionContext: Context of the predictions (country for
            which we are predicting wind energy generation and datetime
            of the prediction).

    Raises:
        ValueError: If `weather_data_df` does not contain one and only
            one row for the `reference_city`.
    """
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

    time = ref_city_data.index.get_level_values("datetime")[0]
    timezone = ref_city_data.iloc[0].loc["timezone"]

    prediction_context = PredictionContext(
        country=country_to_predict, time=time, timezone=timezone
    )

    return features_array, prediction_context


def perform_country_total_wind_energy_prediction(
    features_array: np.array
) -> np.array:
    """
    Loads model and preforms predictions.

    The model uses wind speed data from one reference city (Vannes) to
    predict the total wind energy generation for France.

    The wind energy generation is expressed in MW, and is the energy 
    generated in France by onshore wind turbines during a one-hour
    time slot. 
    If the prediction is made at datetime 8 a.m, the value returned by 
    the model is the total energy generated between 7 a.m and 8 a.m.

    Args:
        features_array (np.array): Preprocessed features.
    
    Returns:
        np.array: The raw model predictions.
    """
    model = _load_model(PRODUCTION_MODEL_PATH)
    return model.predict(features_array)


def postprocess(
    predictions_array: np.array,
    prediction_context: PredictionContext,
) -> pd.DataFrame:
    """
    Transforms raw predictions in a DataFrame ready to be inserted in
    DB.

    Args:
        predictions_array (np.array): Raw model predictions output.
        prediction_context (PredictionContext): Time and country of the
            predictions.

    Returns:
        pd.DataFrame: Formatted predictions.

    Raises:
        ValueError: If the predictions array does not contain one and 
            only one prediction.
    """
    if len(predictions_array) != 1:
        raise ValueError(
            "Postprocessing implemented for only one prediction at a time"
        )
    
    prediction = predictions_array[0]

    return _build_prediction_df(
        prediction_context=prediction_context,
        prediction=prediction,
        unit=PREDICTION_UNIT,
    )
