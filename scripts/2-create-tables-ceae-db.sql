\connect ceae

CREATE TABLE weather_data (
    
    -- index TODO as index
    city VARCHAR(32) NOT NULL,
    country VARCHAR(32) NOT NULL,
    datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    
    -- data
    main VARCHAR(32) NOT NULL,
    description VARCHAR(32) NOT NULL,
    temperature FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL CHECK (wind_speed >= 0),
    wind_dir SMALLINT NOT NULL CHECK (wind_dir >= 0 AND wind_dir <= 360),
    humidity SMALLINT NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    rain_1h NUMERIC(4, 2) NOT NULL CHECK (rain_1h >= 0),
    rain_3h NUMERIC(4, 2) NOT NULL CHECK (rain_3h >= 0),
    clouds SMALLINT NOT NULL CHECK (clouds >= 0 AND clouds <= 100),
    visibility INT NOT NULL CHECK (visibility >= 0),
    timezone INT NOT NULL
);