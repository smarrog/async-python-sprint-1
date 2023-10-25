from typing import Callable, Any
from statistics import mean

from abstract_task import AbstractTask
from day import Day
from city import CityWithDays, CityData

DAYS_FIELD = 'days'
AVERAGE_TEMPERATURE_FIELD = 'temp_avg'
RELEVANT_CONDITIONS_HOURS_FIELD = 'relevant_cond_hours'
AVERAGE_TEMPERATURE_PRECISION = 3


class DataCalculationTask(AbstractTask):
    def __init__(self, data: CityData, calculate_func: Callable[[dict], dict]) -> None:
        self._data = data
        self._calculate_func = calculate_func

    def _run(self) -> Any:
        self.logger.info(f'Calculate data for {self._data.name}.')

        result = self._calculate_func(self._data.data)

        if result is None:
            raise Exception()

        if DAYS_FIELD not in result:
            raise Exception()

        days_data = result[DAYS_FIELD]

        days = []
        for day_data in days_data:
            day_average_temperature = self.__get_average_temperature_for_day(day_data)
            day_relevant_conditions_hours = self.__get_relevant_conditions_hours_for_day(day_data)
            day = Day(day_average_temperature, day_relevant_conditions_hours)
            days.append(day)

        average_temperature = self.__calculate_average_temperature(days)
        relevant_conditions_hours = self.__calculate_relevant_conditions_hours(days)

        city = CityWithDays(self._data.name, average_temperature, relevant_conditions_hours, days)

        self.logger.info(f'Successfully calculated. {city}')

        return city

    def _on_exception(self, exception: Exception):
        self.logger.error(f'Failed to calculate data for {self._data.name}.')
        return None

    @staticmethod
    def __calculate_average_temperature(days: list[Day]) -> float:
        temperatures = map(lambda day: day.average_temperature, days)
        filtered_temperatures = filter(lambda temperature: temperature is not None, temperatures)
        return round(mean(filtered_temperatures), AVERAGE_TEMPERATURE_PRECISION)

    @staticmethod
    def __calculate_relevant_conditions_hours(days: list[Day]) -> int:
        relevant_cond_hours = map(lambda day: day.relevant_conditions_hours, days)
        filtered_relevant_cond_hours = filter(lambda hours: hours is not None, relevant_cond_hours)
        return sum(filtered_relevant_cond_hours)

    @staticmethod
    def __get_average_temperature_for_day(day_info: dict) -> float | None:
        if day_info is None or AVERAGE_TEMPERATURE_FIELD not in day_info:
            return None
        return day_info[AVERAGE_TEMPERATURE_FIELD]

    @staticmethod
    def __get_relevant_conditions_hours_for_day(day_info: dict) -> int | None:
        if day_info is None or RELEVANT_CONDITIONS_HOURS_FIELD not in day_info:
            return None
        return day_info[RELEVANT_CONDITIONS_HOURS_FIELD]
