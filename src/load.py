import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from transform import transform_weather


PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")


def load_weather(row):
    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=10,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO weather (
                    city,
                    weather_time,
                    temperature_c,
                    humidity_pct,
                    precipitation_mm
                )
                VALUES (
                    %(city)s,
                    %(weather_time)s,
                    %(temperature_c)s,
                    %(humidity_pct)s,
                    %(precipitation_mm)s
                )
                -- cette clause permet de mettre à jour les données si elles existent déjà pour la même ville et le même moment.
                ON CONFLICT (city, weather_time)
                DO UPDATE SET
                    temperature_c = EXCLUDED.temperature_c,
                    humidity_pct = EXCLUDED.humidity_pct,
                    precipitation_mm = EXCLUDED.precipitation_mm;
                """,
                row,
            )

    print(f"Données enregistrées : {row['city']} — {row['weather_time']}")


if __name__ == "__main__":
    files = list((PROJECT_DIR / "data" / "raw").glob("paris_*.json"))

    if not files:
        raise FileNotFoundError("Aucun fichier trouvé. Lance extract.py.")

    latest_file = max(files, key=lambda path: path.stat().st_mtime)

    with latest_file.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    row = transform_weather(raw_data, city="Paris")
    load_weather(row)
