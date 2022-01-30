import datetime
import os

from data_fetchers.current_weather import fetch_cities_current_weather
from storage import s3_storage

# config.
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "ceae-bucket"
DUMP_PATH = "data/weather_data.csv"
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
REQUEST_CONFIG_PATH = "config/openweather_cities.yml"


print("--------------")
print(f"Launching pipeline (now='{datetime.datetime.now()}'.")


weather_df = fetch_cities_current_weather(
    request_config_path=REQUEST_CONFIG_PATH,
    api_key=OPENWEATHER_API_KEY,
)

s3_storage.dump_append(
    df=weather_df,
    bucket_name=BUCKET_NAME,
    path=DUMP_PATH,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
