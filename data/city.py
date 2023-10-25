from day import Day
from dataclasses import dataclass


@dataclass
class _CityBase:
    name: str


@dataclass
class CityData(_CityBase):
    data: dict


@dataclass
class City(_CityBase):
    average_temperature: float
    relevant_conditions_hours: int

    def __repr__(self):
        return f'{self.name} [{self.average_temperature}°C, {self.relevant_conditions_hours} good hours]'


@dataclass
class CityWithDays(City):
    days: list[Day]

    def __repr__(self):
        return f'{self.name} [{self.average_temperature}°C, {self.relevant_conditions_hours} good hours]'

    @property
    def total_days(self) -> int | None:
        return len(self.days)

    def get_day(self, day_index: int) -> Day:
        return self.days[day_index]
