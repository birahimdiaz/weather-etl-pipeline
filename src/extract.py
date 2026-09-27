import json
from datetime import datetime, timezone
from pathlib import Path

import requests


def extract_weather(
         city_slug="paris",
         latitude=48.8566,
         longitude=2.3522,
):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "UTC",
    }

    # Interroger l'API et vérifier que la requête a réussi.
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    # Convertir la réponse JSON en dictionnaire Python.
    data = response.json()

    # Trouver le dossier du projet à partir du fichier Python.
    project_dir = Path(__file__).resolve().parent.parent
    raw_dir = project_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Un fichier distinct pour chaque extraction.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    file_path = raw_dir / f"{city_slug}_{timestamp}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Fichier enregistré : {file_path}")
    print(json.dumps(data["current"], indent=2))
    return data

if __name__ == "__main__":
    extract_weather()
