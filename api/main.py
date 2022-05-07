from collections import defaultdict
from typing import List

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
