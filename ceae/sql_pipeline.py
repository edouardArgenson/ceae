import datetime
import os
from string import Template

from sqlalchemy import create_engine

from data_fetchers.current_weather import fetch_cities_current_weather
from storage import sql_storage

# config.
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
REQUEST_CONFIG_PATH = "config/openweather_cities.yml"

db_url_template = Template("$dialect://$user:$password@$host/$dbname")
database_url = db_url_template.substitute(
    dialect=os.environ.get("CEAE_DB_DIALECT"),
    user=os.environ.get("CEAE_DB_USER"),
    password=os.environ.get("CEAE_DB_PASSWORD"),
    host=os.environ.get("CEAE_DB_HOST"),
    dbname=os.environ.get("CEAE_DB_NAME"),
)
print("expected db url: postgresql+psycopg2://ceae:ceae@localhost:5432/ceae")
print(f"got db url: {database_url}")
SQL_ENGINE = create_engine(database_url, echo=True)


print("--------------")
print(f"Launching pipeline (now='{datetime.datetime.now()}'.")


weather_df = fetch_cities_current_weather(
    request_config_path=REQUEST_CONFIG_PATH,
    api_key=OPENWEATHER_API_KEY,
)

sql_storage.dump_append(
    df=weather_df, sql_table_name="weather_data", engine=SQL_ENGINE
)
