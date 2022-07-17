import datetime
from string import Template

import pandas as pd
import requests
import yaml
from sqlalchemy import engine
from storage import sql_storage

URL_TEMPLATE = Template(
    "api.openweathermap.org/data/2.5/weather?q=$city,,$country_code&"
    "units=$units&appid=$api_key"
)


def fetch_cities_current_weather(
    request_config_path: str, api_key: str
) -> pd.DataFrame:
    """Queries openweather current weather API for a list of cities."""
    with open(request_config_path, "r") as stream:
        request_config = yaml.safe_load(stream)

    units = request_config['units']
    cities = request_config['cities']

    fetched_data = []
    for city_item in cities:
        city_name = city_item['name']
        country_code = city_item['country_code']

        url = URL_TEMPLATE.substitute(
            city=city_name,
            country_code=country_code,
            units=units,
            api_key=api_key,
        )

        print(f"requesting data for {city_name}..")

        try:
            response = requests.get("http://" + url)
            response.raise_for_status()
            content = response.json()

            # Looks like we can have several weather
            # groups but never saw it happen, so let's
            # simply take the first one.
            first_weather_group = content["weather"][0]

            rain_data = content.get('rain', None)
            rain_1h = content['rain'].get('1h', 0) if rain_data else 0.
            rain_3h = content['rain'].get('3h', 0) if rain_data else 0.

            data = {
                "main": first_weather_group['main'],
                "description": first_weather_group['description'],
                "temperature" : content['main']['temp'],
                "wind_speed" : content['wind']['speed'],
                "wind_dir" : content['wind']['deg'],
                "humidity": content['main']['humidity'],
                "rain_1h": rain_1h,
                "rain_3h": rain_3h,
                "clouds" : content['clouds']['all'],
                "visibility" : content['visibility'],
                "city" : content['name'],
                "country": content["sys"]["country"],
                "datetime": datetime.datetime.fromtimestamp(content["dt"]),
                "timezone" : content['timezone'],
            }

            print(f"..succesfuly fetched {city_name} data.")
            fetched_data.append(data)

        except requests.exceptions.HTTPError as err:
            print(err)

    return pd.DataFrame(data=fetched_data)


def run_fetch_cities_current_weather_pipeline(
    request_config_path: str, api_key: str, engine: engine.Engine
) -> pd.DataFrame:
    """
    Fetches current weather for all cities in config and store it in 
    DB.
    """
    weather_df = fetch_cities_current_weather(
        request_config_path=request_config_path,
        api_key=api_key,
    )

    sql_storage.dump_append(
        df=weather_df, sql_table_name="weather_data", engine=engine
    )

    return weather_df
