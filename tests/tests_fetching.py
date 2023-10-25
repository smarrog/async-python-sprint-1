import unittest

from fetching import DataFetchingTask

CITY_NAME = 'city_name'
CITY_URL = 'city_url'
FORECASTS_FIELD = 'forecasts'


class FetchingTestCase(unittest.TestCase):
    def test_for_empty_response(self):
        def forecasting(url: str) -> None:
            pass

        task = DataFetchingTask(CITY_NAME, CITY_URL, forecasting)
        city = task.run()

        self.assertIsNone(city)

    def test_for_response_with_no_forecasts_field(self):
        def forecasting(url: str) -> dict:
            return {}

        task = DataFetchingTask(CITY_NAME, CITY_URL, forecasting)
        city = task.run()

        self.assertIsNone(city)

    def test_city_url_is_passed_to_forecasting(self):
        def forecasting(url: str) -> dict:
            return {
                'check': url,
                FORECASTS_FIELD: True
            }

        task = DataFetchingTask(CITY_NAME, CITY_URL, forecasting)
        city = task.run()

        self.assertEqual(CITY_NAME, city.name)
        self.assertEqual(CITY_URL, city.data['check'])
        self.assertTrue(city.data[FORECASTS_FIELD])


if __name__ == '__main__':
    unittest.main()
