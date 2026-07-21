"""
Aplicación principal del laboratorio.

Flujo:
1. Configura logging.
2. Valida rutas.
3. Lee archivo CSV.
4. Procesa información.
5. Calcula métricas.
6. Genera reporte JSON.
"""

import logging

from logger_config import configurar_logging
from proceso import calcular_metricas, leer_ventas
from reportes import exportar_json, generar_reporte
from rutas import CSV_FILE, OUTPUT_FILE, validar_rutas

logger = logging.getLogger("main")


def ejecutar() -> None:
    """
    Ejecuta el flujo completo del procesamiento.
    """

    logger.info("=================================")

    logger.info("Inicio del procesamiento de ventas")

    try:
        # ---------------------------------
        # 1. Validación de rutas
        # ---------------------------------

        validar_rutas()

        logger.debug("Rutas validadas correctamente")

        # ---------------------------------
        # 2. Lectura del CSV
        # ---------------------------------

        ventas = leer_ventas(CSV_FILE)

        logger.info(
            "Ventas cargadas correctamente: %s",
            len(ventas),
        )

        # ---------------------------------
        # 3. Cálculo de métricas
        # ---------------------------------

        metricas = calcular_metricas(ventas)

        logger.info("Métricas calculadas correctamente")

        logger.debug(
            "Métricas obtenidas: %s",
            metricas,
        )

        # ---------------------------------
        # 4. Construcción del reporte
        # ---------------------------------

        reporte = generar_reporte(metricas)

        # ---------------------------------
        # 5. Exportación JSON
        # ---------------------------------

        exportar_json(
            reporte,
            OUTPUT_FILE,
        )

        logger.info(
            "Reporte generado correctamente: %s",
            OUTPUT_FILE,
        )

    except FileNotFoundError as error:
        logger.error(
            "Archivo no encontrado: %s",
            error,
            exc_info=True,
        )

        raise

    except PermissionError as error:
        logger.error(
            "Error de permisos: %s",
            error,
            exc_info=True,
        )

        raise

    except Exception as error:
        logger.critical(
            "Error inesperado durante el procesamiento: %s",
            error,
            exc_info=True,
        )

        raise

    finally:
        logger.info("Fin del procesamiento")

        logger.info("=================================")


def main() -> None:
    """
    Punto de entrada de la aplicación.
    """

    configurar_logging()

    ejecutar()


if __name__ == "__main__":
    main()
