import datetime
from dataclasses import dataclass


@dataclass
class DailyEvent:
    start: datetime.datetime
    duration: int
    title: str
