import unittest

from calculation import DataCalculationTask
from city import CityData

CITY_NAME = 'city_name'
DAYS_FIELD = 'days'
AVERAGE_TEMPERATURE_FIELD = 'temp_avg'
RELEVANT_CONDITIONS_HOURS_FIELD = 'relevant_cond_hours'


class CalculationTestCase(unittest.TestCase):
    def test_for_empty_result(self):
        def calculate(data: dict) -> dict:
            pass

        data = CityData(CITY_NAME, {})
        task = DataCalculationTask(data, calculate)
        city = task.run()

        self.assertIsNone(city)

    def test_for_result_with_no_days_field(self):
        def calculate(data: dict) -> dict:
            return data

        city_data = CityData(CITY_NAME, {})
        task = DataCalculationTask(city_data, calculate)
        city = task.run()

        self.assertIsNone(city)

    def test_correct_result(self):
        def calculate(data: dict) -> dict:
            return data

        raw_data = CityData(CITY_NAME, {
            DAYS_FIELD: [
                {
                    AVERAGE_TEMPERATURE_FIELD: 10,
                    RELEVANT_CONDITIONS_HOURS_FIELD: 5
                },
                {
                    AVERAGE_TEMPERATURE_FIELD: 20,
                    RELEVANT_CONDITIONS_HOURS_FIELD: 7
                }
            ]
        })
        task = DataCalculationTask(raw_data, calculate)
        city = task.run()

        self.assertIsNotNone(city)
        self.assertEqual(CITY_NAME, city.name)
        self.assertEqual(15, city.average_temperature)
        self.assertEqual(12, city.relevant_conditions_hours)
        self.assertEqual(2, city.total_days)
        self.assertEqual(10, city.get_day(0).average_temperature)
        self.assertEqual(5, city.get_day(0).relevant_conditions_hours)
        self.assertEqual(20, city.get_day(1).average_temperature)
        self.assertEqual(7, city.get_day(1).relevant_conditions_hours)


if __name__ == '__main__':
    unittest.main()
