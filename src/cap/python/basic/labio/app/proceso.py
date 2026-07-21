"""
Módulo encargado del procesamiento de ventas.

Responsabilidades:
- Lectura del CSV.
- Conversión de datos.
- Validación de registros.
- Cálculo de métricas.
"""

import csv
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("procesador")


def leer_ventas(
    path: Path,
) -> list[dict[str, Any]]:
    """
    Lee el archivo CSV de ventas.

    Convierte cada fila en un diccionario
    con tipos de datos correctos.

    Args:
        path:
            Ruta del archivo CSV.

    Returns:
        Lista de ventas procesadas.
    """

    logger.info(
        "Iniciando lectura del archivo CSV: %s",
        path,
    )

    ventas: list[dict[str, Any]] = []

    try:
        with path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as archivo:
            reader = csv.DictReader(archivo)

            for numero_linea, row in enumerate(
                reader,
                start=2,
            ):
                try:
                    venta = convertir_venta(row)

                    ventas.append(venta)

                except (
                    ValueError,
                    KeyError,
                ) as error:
                    logger.warning(
                        "Registro inválido en línea %s: %s",
                        numero_linea,
                        error,
                    )

        logger.info(
            "CSV leído correctamente. Registros válidos: %s",
            len(ventas),
        )

        return ventas

    except FileNotFoundError:
        logger.error(
            "No existe el archivo CSV: %s",
            path,
            exc_info=True,
        )

        raise

    except Exception as error:
        logger.error(
            "Error leyendo archivo CSV: %s",
            error,
            exc_info=True,
        )

        raise


def convertir_venta(
    row: dict[str, str],
) -> dict[str, Any]:
    """
    Convierte una fila del CSV
    a un registro con tipos correctos.

    Args:
        row:
            Registro leído por DictReader.

    Returns:
        Venta convertida.
    """

    return {
        "id": int(row["id"]),
        "producto": row["producto"],
        "categoria": row["categoria"],
        "cantidad": int(row["cantidad"]),
        "precio": float(row["precio"]),
    }


def calcular_metricas(
    ventas: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Calcula métricas generales
    de las ventas procesadas.

    Args:
        ventas:
            Lista de ventas.

    Returns:
        Diccionario con métricas.
    """

    logger.info("Calculando métricas de ventas")

    total_registros = len(ventas)

    total_unidades = sum(venta["cantidad"] for venta in ventas)

    ingresos_totales = sum(venta["cantidad"] * venta["precio"] for venta in ventas)

    productos = len({venta["producto"] for venta in ventas})

    metricas = {
        "ventas_procesadas": total_registros,
        "productos_diferentes": productos,
        "unidades_vendidas": total_unidades,
        "ingresos_totales": round(
            ingresos_totales,
            2,
        ),
    }

    logger.debug(
        "Métricas calculadas: %s",
        metricas,
    )

    return metricas
