# ceae

An exploratory project that:
- Fetch and store current weather data from openweathermap.org (https://openweathermap.org/current).
- Expose those data with an API.
- Runs a (dummy) ML pipeline to predict the total wind energy generated during the last hour in France (using the wind from the weather data). Predictions are also exposed in the API.

### Structure

Two services:
- `ceae` that performs the weather data fetching and storage and the ML pipeline. It is meant to be run at regular intervals (for instance every 20 minutes).
- `api` the API built with `fastapi` https://fastapi.tiangolo.com/.

A (containerized) postgresql database.

The services use `SQLAlchemy` (https://www.sqlalchemy.org/) to communicate with the database.

### Current weather data.

The data is fetched via API calls on https://openweathermap.org/current (free api).
The `/config` directory contains a yaml listing some cities for which we query the weather.
For each city, a call to openweather gives current weather data, like temperature, wind speed, etc..
The fetched data is stored in the database.

### Wind energy generation predictions.

The pipeline contains a dummy model that try to predict the total onshore wind energy (in MW) generated in France during the last one-hour time slot.
The model is a linear regression. The only feature is the wind speed from one city in France (serves as a proxy for a global amount of wind in France) taken at the time of the prediction.
The model was trained on one month of data (hourly frequency), using open-source target data from RTE (https://data.rte-france.com/catalog/-/api/generation/Actual-Generation/v1.1).

### Running the code locally.

The project runs with Docker using Docker Compose.

1. Pull the repo.

2. You need to get an openweather api key and add it in the config files.

You can get a free api key there: https://openweathermap.org/price.

Add a `config/openweather-api-key.env` file containing your key, for instance:
```
OPENWEATHER_API_KEY=uselessfakekey
```

3. Build the images:

`DOCKER_BUILDKIT=1 docker build . -f ceae/Dockerfile -t ceae --target runtime`.

`DOCKER_BUILDKIT=1 docker build . -f api/Dockerfile -t ceae-api --target runtime`.

4. Launch the services: `docker compose up`.

5. You can then check the API on http://127.0.0.1/docs#/.

Note: there is currently an issue with `docker compose up --build` as the `ceae` service is lauched too early (database not ready).
