import datetime
from collections import defaultdict

from typing import DefaultDict, List, Optional

from .events import DailyEvent

from jours_feries_france import JoursFeries
from vacances_scolaires_france import SchoolHolidayDates


def collect_french_holidays(
    year: int,
    events: DefaultDict[str, DefaultDict[str, List[DailyEvent]]],
    school_zone: Optional[str],
    bank_zone: Optional[str],
):
    school_holidays = (
        SchoolHolidayDates().holidays_for_year_and_zone(year, school_zone)
        if school_zone
        else None
    )
    bank_holidays: Optional[DefaultDict[datetime.date, List[str]]] = (
        defaultdict(list) if bank_zone else None
    )
    if bank_holidays is not None:
        for name, d in JoursFeries.for_year(year, bank_zone).items():
            bank_holidays[d].append(name)

    timestamp_key = "00:00"
    # means full day…

    for mon in range(1, 12 + 1):
        for day in range(1, 31 + 1):
            try:
                date = datetime.date(year, mon, day)
            except (TypeError, ValueError):
                continue

            if school_holidays and date in school_holidays:
                holiday = school_holidays[date]
                date_key = date.isoformat()
                events[date_key][timestamp_key].append(
                    DailyEvent(
                        datetime.datetime(date.year, date.month, date.day),
                        0,
                        holiday.get("nom_vacances", ""),
                    )
                )

            if bank_holidays and date in bank_holidays:
                date_key = date.isoformat()
                for title in bank_holidays[date]:
                    events[date_key][timestamp_key].append(
                        DailyEvent(
                            datetime.datetime(date.year, date.month, date.day),
                            0,
                            title,
                        )
                    )
