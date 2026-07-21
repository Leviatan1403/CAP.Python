"""
Módulo encargado de generar y exportar reportes.
"""

import json
import logging
from pathlib import Path
from typing import Any

from fecha import obtener_fecha_actual

logger = logging.getLogger("reportes")


def generar_reporte(
    metricas: dict[str, Any],
) -> dict[str, Any]:

    logger.info("Generando estructura del reporte")

    reporte = {
        "fecha_generacion": obtener_fecha_actual(),
        "metricas": metricas,
    }

    logger.debug(
        "Reporte generado: %s",
        reporte,
    )

    return reporte


def exportar_json(
    reporte: dict[str, Any],
    output: Path,
) -> None:

    logger.info(
        "Exportando reporte JSON: %s",
        output,
    )

    with output.open(
        mode="w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            reporte,
            archivo,
            indent=4,
            ensure_ascii=False,
        )

    logger.info("Reporte exportado correctamente")
