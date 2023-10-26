import logging
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from tasks import AbstractTask, DataFetchingTask, DataCalculationTask, DataAnalyzingTask, DataAggregationTask
from data import CityWithDays, CityData, City
from utils import CITIES, get_url_by_city_name
from typing import Iterator, Any
from external.client import YandexWeatherAPI
from external.analyzer import analyze_json as calculate_city_data
from log_settings import init as init_logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(ROOT_DIR, 'output')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'database.json')

FETCH_MILESTONE = 'FETCH'
CALCULATE_MILESTONE = 'CALCULATE'
AGGREGATE_MILESTONE = 'AGGREGATE'
ANALYZE_MILESTONE = 'ANALYZE'
RESULT_MILESTONE = 'RESULT'

USE_MULTIPLE_PROCESSES = True
MAX_THREADS = 10

logger = logging.getLogger()


def forecast_weather() -> None:
    cities_data = fetch()
    cities = calculate(cities_data)
    aggregate(cities)
    best_cities = analyze()
    show_result(best_cities)


def fetch() -> Iterator[CityData]:
    log_milestone(FETCH_MILESTONE)

    tasks = (
        DataFetchingTask(city_name, get_url_by_city_name(city_name), YandexWeatherAPI.get_forecasting)
        for city_name in CITIES)

    return filter(lambda city_data: city_data is not None, run_tasks_in_multiple_threads(tasks))


def calculate(cities_data: Iterator[CityData]) -> Iterator[CityWithDays]:
    log_milestone(CALCULATE_MILESTONE)

    tasks = (
        DataCalculationTask(city_data, calculate_city_data)
        for city_data in cities_data)

    return filter(lambda city: city is not None, run_tasks_in_multiple_processes(tasks))


def aggregate(cities: Iterator[CityWithDays]) -> None:
    log_milestone(AGGREGATE_MILESTONE)

    os.makedirs(DATABASE_DIR, exist_ok=True)

    task = DataAggregationTask(cities, DATABASE_PATH)
    task.run()


def analyze() -> list[City]:
    log_milestone(ANALYZE_MILESTONE)

    task = DataAnalyzingTask(DATABASE_PATH)
    return task.run()


def show_result(best_cities: list[City]) -> None:
    log_milestone(RESULT_MILESTONE)

    if len(best_cities) == 0:
        logger.info(f'NO CITIES')
    else:
        for city_result in best_cities:
            logger.info(f'{city_result}')


def log_milestone(name: str) -> None:
    logger.info(f'===========================> {name} <===========================')


def run_task(task: AbstractTask) -> Any:
    return task.run()


def run_task_in_other_process(task: AbstractTask) -> Any:
    init_logging()
    return run_task(task)


def run_tasks_in_multiple_threads(tasks: Iterator[AbstractTask]) -> Iterator[Any]:
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as threads_pool:
        results = threads_pool.map(run_task, tasks)
    return results


def run_tasks_in_multiple_processes(tasks: Iterator[AbstractTask]) -> Iterator[Any]:
    processes_amount = get_max_processes()
    if processes_amount == 1:
        results = (task.run() for task in tasks)
        return results

    with multiprocessing.Pool(processes=processes_amount) as pool:
        results = pool.map(run_task_in_other_process, tasks)
    return results


def get_max_processes():
    if USE_MULTIPLE_PROCESSES:
        return multiprocessing.cpu_count()
    else:
        return 1


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')

    init_logging()
    forecast_weather()
