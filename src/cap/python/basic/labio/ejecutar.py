"""
Script de automatización del procesamiento de ventas.

Este módulo ejecuta la aplicación principal
utilizando subprocess.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

APP_FILE = BASE_DIR / "app" / "main.py"


def ejecutar_proceso() -> int:
    """
    Ejecuta la aplicación principal
    y devuelve el código de salida.
    """

    print("Iniciando proceso automático...")

    try:
        resultado = subprocess.run(
            [
                sys.executable,
                str(APP_FILE),
            ],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
        )

        print("\n--- SALIDA DEL PROCESO ---")

        print(resultado.stdout)

        if resultado.stderr:
            print("\n--- ERRORES ---")

            print(resultado.stderr)

        if resultado.returncode == 0:
            print("\nProceso finalizado correctamente.")

        else:
            print("\nEl proceso terminó con errores.")

        return resultado.returncode

    except FileNotFoundError as error:
        print(f"No se encontró el archivo: {error}")

        return 1

    except Exception as error:
        print(f"Error ejecutando proceso: {error}")

        return 1


def main() -> None:
    """
    Punto de entrada del script.
    """

    codigo = ejecutar_proceso()

    sys.exit(codigo)


if __name__ == "__main__":
    main()
