import datetime as dt
from typing import List

from pydantic import BaseModel


class City(BaseModel):
    name: str


class Country(BaseModel):
    code: str
    cities: List[City]


class Weather(BaseModel):
    datetime: dt.datetime
    timezone: int
    main: str
    description: str
    temperature: float
    wind_speed: float
    wind_dir: float
    humidity: int
    rain_1h: float
    rain_3h: float
    clouds: int
    visibility: int

    class Config:
        orm_mode = True
