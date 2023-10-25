import os
import unittest
import json

from aggregation import DataAggregationTask
from city import CityWithDays
from day import Day

CITY_NAME_1 = 'city_name_1'
CITY_NAME_2 = 'city_name_2'

NAME_FIELD = 'name'
AVERAGE_TEMPERATURE_FIELD = 'average_temperature'
RELEVANT_CONDITIONS_FIELD = 'relevant_conditions_hours'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(ROOT_DIR, 'output')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'tmp.json')


class AggregationTestCase(unittest.TestCase):
    os.makedirs(DATABASE_DIR, exist_ok=True)

    def test_write_and_read(self):
        cities = [
            CityWithDays(CITY_NAME_1, 10, 5, [Day(9, 2), Day(11, 3)]),
            CityWithDays(CITY_NAME_2, 13.5, 3, [Day(10, 2), Day(17, 1)])
        ]

        task = DataAggregationTask((city for city in cities), DATABASE_PATH)
        task.run()

        self.assertTrue(os.path.exists(DATABASE_PATH))

        with open(DATABASE_PATH, 'r') as f:
            database = json.load(f)

        self.assertEqual(database[0][NAME_FIELD], CITY_NAME_2)
        self.assertEqual(database[0][AVERAGE_TEMPERATURE_FIELD], 13.5)
        self.assertEqual(database[0][RELEVANT_CONDITIONS_FIELD], 3)

        self.assertEqual(database[1][NAME_FIELD], CITY_NAME_1)
        self.assertEqual(database[1][AVERAGE_TEMPERATURE_FIELD], 10)
        self.assertEqual(database[1][RELEVANT_CONDITIONS_FIELD], 5)




if __name__ == '__main__':
    unittest.main()
