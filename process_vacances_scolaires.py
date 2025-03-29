import datetime
import csv
import logging
from pathlib import Path
from typing import Any, Dict

CSV_PATH = "vacances-scolaires/data.csv"

LOGGER = logging.getLogger()


def create_entry(entries: Dict[str, Any], date: datetime.date, title: str):
    ymd = date.strftime("%Y-%m-%d")
    hms = "00:00"

    if ymd not in entries:
        entries[ymd] = {}
    day = entries[ymd]
    if hms not in day:
        day[hms] = []

    day[hms].append([0, title])


def _zone_key(zone: str) -> str:
    zones = {"A": "vacances_zone_a", "B": "vacances_zone_b", "C": "vacances_zone_c"}
    return zones[zone]


def collect_holidays(year, entries, *, zone: str):
    zone_key = _zone_key(zone)
    csv_path = Path(CSV_PATH)
    if not csv_path.exists():
        LOGGER.warning("Skipping collect of French holidays")
        return

    with open(csv_path) as input_str:
        reader = csv.DictReader(input_str, delimiter=",")
        for row in reader:
            raw_date = row.get("date")
            if raw_date is None:
                raise RuntimeError("Unexpected date value")

            date = datetime.date.fromisoformat(raw_date)
            if date.year != year:
                continue

            is_holiday = row.get(zone_key) == "True"
            if not is_holiday:
                continue

            title = row.get("nom_vacances")
            if title is None:
                raise RuntimeError("Unexpected title value")

            create_entry(entries, date, title)
