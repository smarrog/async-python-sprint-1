from typing import Callable

from abstract_task import AbstractTask
from city import CityData
from exceptions import EmptyFetchResponseException, InvalidFetchResponseException

FORECASTS_FIELD = 'forecasts'


class DataFetchingTask(AbstractTask):
    def __init__(self, city_name: str, city_url: str, get_forecasting: Callable) -> None:
        self._city_name = city_name
        self._city_url = city_url
        self._get_forecasting = get_forecasting

    def _run(self) -> CityData:
        self.logger.info('Fetching data for %s.', self._city_name)

        response = self._get_forecasting(self._city_url)

        if response is None:
            raise EmptyFetchResponseException()
        if FORECASTS_FIELD not in response:
            raise InvalidFetchResponseException()

        self.logger.info('Successfully got data for %s.', self._city_name)
        return CityData(self._city_name, response)

    def _on_exception(self, exception: Exception):
        self.logger.error('Failed to fetch data for %s.', self._city_name)
        return None
