from sqlalchemy import CheckConstraint, Column, MetaData, and_, column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import (
    FLOAT, INTEGER, NUMERIC, SMALLINT, TIMESTAMP, VARCHAR
)


# declarative base class
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_N_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
Base = declarative_base(metadata=meta)

class WeatherData(Base):
    __tablename__ = "weather_data"

    city = Column(VARCHAR(length=32), primary_key=True)
    country = Column(VARCHAR(length=32), primary_key=True)
    datetime = Column(TIMESTAMP(timezone=False), primary_key=True)
    
    main = Column(VARCHAR(length=32), nullable=False)
    description = Column(VARCHAR(length=32), nullable=False)
    temperature = Column(FLOAT, nullable=False)
    wind_speed = Column(FLOAT, CheckConstraint(column("wind_speed") >= 0), nullable=False)
    wind_dir = Column(
        SMALLINT,
        CheckConstraint(and_(column("wind_dir") >= 0, column("wind_dir") <= 360)),
        nullable=False,
    )
    humidity = Column(
        SMALLINT, 
        CheckConstraint(and_(column("humidity") >= 0, column("humidity") <= 100)),
        nullable=False,
    )
    rain_1h = Column(
        NUMERIC(precision=4, scale=2),
        CheckConstraint(column("rain_1h") >= 0),
        nullable=False,
    )
    rain_3h = Column(
        NUMERIC(precision=4, scale=2),
        CheckConstraint(column("rain_3h") >= 0),
        nullable=False,
    )
    clouds = Column(
        SMALLINT,
        CheckConstraint(and_(column("clouds") >= 0, column("clouds") <= 100)),
        nullable=False,
    )
    visibility = Column(INTEGER, CheckConstraint(column("visibility") >= 0), nullable=False)
    timezone = Column(INTEGER, nullable=False)
