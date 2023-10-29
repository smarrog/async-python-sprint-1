import json

from abstract_task import AbstractTask
from city import City

NAME_FIELD = 'name'
AVERAGE_TEMPERATURE_FIELD = 'average_temperature'
RELEVANT_CONDITIONS_FIELD = 'relevant_conditions_hours'


class DataAnalyzingTask(AbstractTask):
    def __init__(self, database_path: str) -> None:
        self._database_path = database_path

    def _run(self) -> list[City]:
        self.logger.info(f'Analyze')

        with open(self._database_path, 'r') as f:
            database = json.load(f)

        best_cities = self.get_best_cities(database)

        self.logger.info('Analyze was successfully finished')

        return best_cities

    def _on_exception(self, exception: Exception):
        self.logger.error('Failed to analyze')

    @staticmethod
    def get_best_cities(database: list) -> list[City]:
        results = list[City]()
        last_result: None | City = None
        for city_data in database:
            if last_result is not None:
                if city_data[AVERAGE_TEMPERATURE_FIELD] != last_result.average_temperature:
                    break

                if city_data[RELEVANT_CONDITIONS_FIELD] != last_result.relevant_conditions_hours:
                    break

            city_result = City(
                city_data[NAME_FIELD],
                city_data[AVERAGE_TEMPERATURE_FIELD],
                city_data[RELEVANT_CONDITIONS_FIELD])

            results.append(city_result)
            last_result = city_result

        return results
