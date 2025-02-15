import dataclasses
import datetime


@dataclasses.dataclass
class ActionLog:
    id: int
    type_name: str
    date: datetime.datetime
    comment: str
    is_forecast: bool


@dataclasses.dataclass
class ActionLogType:
    category: str
    name: str
    interval: int
    next: str
