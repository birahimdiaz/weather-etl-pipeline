from datetime import timedelta

import pendulum
from airflow.sdk import dag, task, task_group


CITIES = [
    {
        "name": "Paris",
        "slug": "paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
    },
    {
        "name": "Dakar",
        "slug": "dakar",
        "latitude": 14.7167,
        "longitude": -17.4677,
    },
]


@dag(
    dag_id="weather_etl",
    schedule="0 * * * *",
    start_date=pendulum.datetime(2026, 9, 26, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["weather", "etl"],
)
def weather_etl():

    @task()
    def extract(city):
        from extract import extract_weather

        return extract_weather(
            city_slug=city["slug"],
            latitude=city["latitude"],
            longitude=city["longitude"],
        )

    @task()
    def transform(raw_data, city_name):
        from transform import transform_weather

        return transform_weather(raw_data, city=city_name)

    @task()
    def load(row):
        from load import load_weather

        load_weather(row)

    @task_group()
    def city_pipeline(city):
        raw_data = extract(city)
        cleaned_data = transform(raw_data, city["name"])
        load(cleaned_data)

    for city in CITIES:
        city_pipeline.override(group_id=city["slug"])(city)


weather_etl()