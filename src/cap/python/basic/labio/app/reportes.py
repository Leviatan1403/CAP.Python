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
    """
    Genera la estructura final del reporte.

    Agrega la fecha de generación
    utilizando la zona horaria configurada.

    Args:
        metricas:
            Métricas calculadas del proceso.

    Returns:
        Reporte listo para exportar.
    """

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
    """
    Exporta el reporte a un archivo JSON.

    Args:
        reporte:
            Datos del reporte.

        output:
            Ruta del archivo JSON.
    """

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
