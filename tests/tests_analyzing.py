import unittest
import os
import json

from analyzing import DataAnalyzingTask
from city import City

NAME_FIELD = 'name'
AVERAGE_TEMPERATURE_FIELD = 'average_temperature'
RELEVANT_CONDITIONS_FIELD = 'relevant_conditions_hours'

CITY_NAME_1 = 'city_name_1'
CITY_NAME_2 = 'city_name_2'
CITY_NAME_3 = 'city_name_3'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(ROOT_DIR, 'output')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'tmp.json')


class AnalyzingTestCase(unittest.TestCase):
    def test_positive_single_result(self):
        database = [
            {
                NAME_FIELD: CITY_NAME_1,
                AVERAGE_TEMPERATURE_FIELD: 10,
                RELEVANT_CONDITIONS_FIELD: 12
            },
            {
                NAME_FIELD: CITY_NAME_2,
                AVERAGE_TEMPERATURE_FIELD: 5,
                RELEVANT_CONDITIONS_FIELD: 3
            }
        ]

        with open(DATABASE_PATH, 'w') as f:
            json.dump(database, f, indent=4, ensure_ascii=False)

        task = DataAnalyzingTask(DATABASE_PATH)
        results: list[City] = task.run()

        self.assertEqual(1, len(results))
        self.assertEqual(CITY_NAME_1, results[0].name)
        self.assertEqual(10, results[0].average_temperature)
        self.assertEqual(12, results[0].relevant_conditions_hours)

    def test_positive_multiple_results(self):
        database = [
            {
                NAME_FIELD: CITY_NAME_1,
                AVERAGE_TEMPERATURE_FIELD: 10,
                RELEVANT_CONDITIONS_FIELD: 12
            },
            {
                NAME_FIELD: CITY_NAME_2,
                AVERAGE_TEMPERATURE_FIELD: 10,
                RELEVANT_CONDITIONS_FIELD: 12
            },
            {
                NAME_FIELD: CITY_NAME_3,
                AVERAGE_TEMPERATURE_FIELD: 10,
                RELEVANT_CONDITIONS_FIELD: 9
            }
        ]

        with open(DATABASE_PATH, 'w') as f:
            json.dump(database, f, indent=4, ensure_ascii=False)

        task = DataAnalyzingTask(DATABASE_PATH)
        results: list[City] = task.run()

        self.assertEqual(2, len(results))
        self.assertEqual(CITY_NAME_1, results[0].name)
        self.assertEqual(10, results[0].average_temperature)
        self.assertEqual(12, results[0].relevant_conditions_hours)
        self.assertEqual(CITY_NAME_2, results[1].name)
        self.assertEqual(10, results[1].average_temperature)
        self.assertEqual(12, results[1].relevant_conditions_hours)


if __name__ == '__main__':
    unittest.main()
