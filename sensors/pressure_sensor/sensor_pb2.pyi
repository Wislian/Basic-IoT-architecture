from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SensorData(_message.Message):
    __slots__ = ("sensor_id", "person_id", "systolic_pressure", "diastolic_pressure", "unit", "date")
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    PERSON_ID_FIELD_NUMBER: _ClassVar[int]
    SYSTOLIC_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    DIASTOLIC_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    sensor_id: str
    person_id: int
    systolic_pressure: float
    diastolic_pressure: float
    unit: str
    date: str
    def __init__(self, sensor_id: _Optional[str] = ..., person_id: _Optional[int] = ..., systolic_pressure: _Optional[float] = ..., diastolic_pressure: _Optional[float] = ..., unit: _Optional[str] = ..., date: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
