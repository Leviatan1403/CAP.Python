import logging.config
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "config" / "logging.yaml"

LOG_DIR = BASE_DIR / "logs"


def configurar_logging() -> None:

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with CONFIG_FILE.open(
        encoding="utf-8",
    ) as archivo:
        configuracion = yaml.safe_load(archivo)

    # Convertir ruta relativa del YAML
    # en ruta absoluta

    configuracion["handlers"]["archivo"]["filename"] = str(LOG_DIR / "proceso.log")

    logging.config.dictConfig(configuracion)
