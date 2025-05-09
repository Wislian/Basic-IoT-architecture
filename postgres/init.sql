CREATE TABLE IF NOT EXISTS Person (
    Id SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Phone VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Sensors (
    SensorId VARCHAR(10) PRIMARY KEY,
    SensorStatus VARCHAR(20) NOT NULL,
    Unit VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS Temperature (
    TemperatureId SERIAL PRIMARY KEY,
    PersonId INT NOT NULL,
    SensorId VARCHAR(10) NOT NULL,
    TemperatureValue FLOAT NOT NULL,
    Unit VARCHAR(3) NOT NULL,
    RegisterDate TIMESTAMP NOT NULL,
    CONSTRAINT fk_temperature_person FOREIGN KEY (PersonId) REFERENCES Person(Id),
    CONSTRAINT fk_temperature_sensor FOREIGN KEY (SensorId) REFERENCES Sensors(SensorId)
);

CREATE TABLE IF NOT EXISTS HeartRate (
    HeartRateId SERIAL PRIMARY KEY,
    PersonId INT NOT NULL,
    SensorId VARCHAR(10) NOT NULL,
    HeartRateValue INT NOT NULL,
    Unit VARCHAR(5) NOT NULL,
    RegisterDate TIMESTAMP NOT NULL,
    CONSTRAINT fk_heartrate_person FOREIGN KEY (PersonId) REFERENCES Person(Id),
    CONSTRAINT fk_heartrate_sensor FOREIGN KEY (SensorId) REFERENCES Sensors(SensorId)
);

CREATE TABLE IF NOT EXISTS BloodPressure (
    BloodPressureId SERIAL PRIMARY KEY,
    PersonId INT NOT NULL,
    SensorId VARCHAR(10) NOT NULL,
    SystolicPressure INT NOT NULL,
    DiastolicPressure INT NOT NULL,
    Unit VARCHAR(6) NOT NULL,
    RegisterDate TIMESTAMP NOT NULL,
    CONSTRAINT fk_bloodpressure_person FOREIGN KEY (PersonId) REFERENCES Person(Id),
    CONSTRAINT fk_bloodpressure_sensor FOREIGN KEY (SensorId) REFERENCES Sensors(SensorId)
);