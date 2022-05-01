from typing import List

from pydantic import BaseModel


class City(BaseModel):
    name: str


class Country(BaseModel):
    code: str
    cities: List[City]
