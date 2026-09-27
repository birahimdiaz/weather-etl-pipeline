import logging

from extract import extract_weather
from transform import transform_weather
from load import load_weather


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Début de l'extraction")
    raw_data = extract_weather()

    logger.info("Début de la transformation")
    row = transform_weather(raw_data, city="Paris")

    logger.info("Début du chargement")
    load_weather(row)

    logger.info("Pipeline terminé avec succès")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception:
        logger.exception("Échec du pipeline")
        raise
