import json
from typing import Any, Iterator

from abstract_task import AbstractTask
from city import CityWithDays

NAME_FIELD = 'name'
DAYS_FIELD = 'days'
AVERAGE_TEMPERATURE_FIELD = 'average_temperature'
RELEVANT_CONDITIONS_FIELD = 'relevant_conditions_hours'


class DataAggregationTask(AbstractTask):
    def __init__(self, cities: Iterator[CityWithDays], database_path: str) -> None:
        self._cities = cities
        self._database_path = database_path

    def _run(self) -> Any:
        self.logger.info('Aggregate data.')

        sorted_cities = sorted(self._cities, key=lambda e: (-e.average_temperature, -e.relevant_conditions_hours))

        database = []
        for city_index in range(0, len(sorted_cities)):
            city = sorted_cities[city_index]

            days_in_database = []
            for day_index in range(0, city.total_days):
                days_in_database.append({
                    AVERAGE_TEMPERATURE_FIELD: city.get_day(day_index).average_temperature,
                    RELEVANT_CONDITIONS_FIELD: city.get_day(day_index).relevant_conditions_hours
                })

            database.append({
                NAME_FIELD: city.name,
                AVERAGE_TEMPERATURE_FIELD: city.average_temperature,
                RELEVANT_CONDITIONS_FIELD: city.relevant_conditions_hours,
                DAYS_FIELD: days_in_database
            })

        with open(self._database_path, 'w') as f:
            json.dump(database, f, indent=4, ensure_ascii=False)

        self.logger.info('Data for was aggregated. Database was written to %s', self._database_path)

    def _on_exception(self, exception: Exception):
        self.logger.exception('Failed to aggregate data.')
