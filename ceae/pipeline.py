import datetime
import os

from data_fetchers.current_weather import fetch_cities_current_weather
from storage import filesystem_storage

# config.
DUMP_PATH = "data/weather_data.csv"
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
REQUEST_CONFIG_PATH = "config/openweather_cities.yml"


print("--------------")
print(f"Launching pipeline (now='{datetime.datetime.now()}'.")

weather_df = fetch_cities_current_weather(
    request_config_path=REQUEST_CONFIG_PATH,
    api_key=OPENWEATHER_API_KEY,
)

filesystem_storage.dump_append(
    df=weather_df,
    dump_path=DUMP_PATH,
)
