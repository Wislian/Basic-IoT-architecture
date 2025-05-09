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
    CONSTRAINT fk_Heartrate_person FOREIGN KEY (PersonId) REFERENCES Person(Id),
    CONSTRAINT fk_Heartrate_sensor FOREIGN KEY (SensorId) REFERENCES Sensors(SensorId)
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

INSERT INTO Person (Id, FirstName, LastName, Phone) VALUES
(1, 'Luis', 'González', '3001234567'),
(2, 'María', 'Pérez', '3012345678'),
(3, 'Carlos', 'Ramírez', '3023456789'),
(4, 'Ana', 'Martínez', '3034567890');

INSERT INTO Sensors (SensorId, SensorStatus, Unit) VALUES
('Temp_001', 'active', 'C'),
('Temp_002', 'active', 'C'),
('Temp_003', 'active', 'C'),

('Press_001', 'active', 'mmHg'),
('Press_002', 'active', 'mmHg'),
('Press_003', 'active', 'mmHg'),

('Heart_001', 'active', 'bpm'),
('Heart_002', 'active', 'bpm'),
('Heart_003', 'active', 'bpm');
