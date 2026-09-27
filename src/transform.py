import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def transform_weather(data, city):
    current = data["current"]

    # Rendre explicite le fuseau horaire fourni par l'API.
    source_timezone = timezone(
        timedelta(seconds=data["utc_offset_seconds"])
    )
    weather_time = datetime.fromisoformat(current["time"])
    weather_time = weather_time.replace(tzinfo=source_timezone)

    # Vérifier la présence et le type des valeurs.
    fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
    ]

    for field in fields:
        value = current.get(field)
        if type(value) not in (int, float):
            raise ValueError(f"Valeur absente ou non numérique : {field}")

    if not 0 <= current["relative_humidity_2m"] <= 100:
        raise ValueError("L'humidité doit être comprise entre 0 et 100")

    if current["precipitation"] < 0:
        raise ValueError("Les précipitations ne peuvent pas être négatives")

    # Construire une ligne prête pour le stockage.
    return {
        "city": city,
        "weather_time": weather_time.astimezone(timezone.utc).isoformat(),
        "temperature_c": float(current["temperature_2m"]),
        "humidity_pct": float(current["relative_humidity_2m"]),
        "precipitation_mm": float(current["precipitation"]),
    }


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent.parent
    raw_dir = project_dir / "data" / "raw"
    files = list(raw_dir.glob("paris_*.json"))

    if not files:
        raise FileNotFoundError("Aucun fichier trouvé. Lance extract.py.")

    latest_file = max(files, key=lambda path: path.stat().st_mtime)

    with latest_file.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    result = transform_weather(raw_data, city="Paris")
    print(json.dumps(result, indent=2, ensure_ascii=False))
