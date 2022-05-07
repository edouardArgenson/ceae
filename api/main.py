import datetime as dt
from collections import defaultdict
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

ceae_api = FastAPI()


# Dependency
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@ceae_api.get("/countries", response_model=List[schemas.Country])
def countries_with_cities(session: Session = Depends(get_session)):
    countries_qs = crud.get_countries_with_cities(session=session)

    cities_by_country = defaultdict(list)
    for q in countries_qs:
        cities_by_country[q.country].append({"name": q.city})

    return [
        {"code": country_name, "cities": cities}
        for country_name, cities in cities_by_country.items()
    ]


@ceae_api.get("/countries/{country_code}", response_model=schemas.Country)
def country_with_cities(
    country_code: str, session: Session = Depends(get_session)
):
    countries_qs = crud.get_country_with_cities(
        country_code=country_code, session=session
    )
    if len(countries_qs) == 0:
        raise HTTPException(status_code=404, detail="Country not found.")
    return {
        "code": country_code,
        "cities": [{"name": q.city} for q in countries_qs]
    }


@ceae_api.get(
    "/countries/{country_code}/cities", response_model=List[schemas.City]
)
def cities(
    country_code: str, session: Session = Depends(get_session)
):
    countries_qs = crud.get_country_with_cities(
        country_code=country_code, session=session
    )
    if len(countries_qs) == 0:
        raise HTTPException(status_code=404, detail="Country not found.")
    return [{"name": q.city} for q in countries_qs]


@ceae_api.get(
    "/countries/{country_code}/cities/{city_name}",
    response_model=schemas.City,
)
def city(
    country_code: str, city_name: str, session: Session = Depends(get_session)
):
    cities_qs = crud.get_city(
        country_code=country_code, city_name=city_name, session=session
    )
    if len(cities_qs) == 0:
        raise HTTPException(status_code=404, detail="City not found.")
    return [{"name": q.city} for q in cities_qs][0]


@ceae_api.get(
    "/countries/{country_code}/cities/{city_name}/weather",
    response_model=List[schemas.Weather],
)
def weather(
    country_code: str,
    city_name: str,
    start_date: Optional[dt.datetime] = None,
    end_date: Optional[dt.datetime] = None,
    session: Session = Depends(get_session),
):
    cities_qs = crud.get_city(
        country_code=country_code, city_name=city_name, session=session
    )
    if len(cities_qs) == 0:
        raise HTTPException(status_code=404, detail="City not found.")

    return crud.get_weather(
        country_code=country_code,
        city_name=city_name,
        start_date=start_date,
        end_date=end_date,
        session=session,
    )
