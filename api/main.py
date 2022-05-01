from collections import defaultdict
from typing import List

from fastapi import Depends, FastAPI
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
