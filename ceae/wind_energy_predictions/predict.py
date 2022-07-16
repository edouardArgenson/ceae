import joblib
from sklearn.base import BaseEstimator


def _load_model(model_path: str) -> BaseEstimator:
    return joblib.load(model_path)
