from io import open
import json
import os
import pathlib

from funciones.filtroAlumnos import filtroalumnos

# Obtiene la ruta de la carpeta del script actual
carpeta_actual = pathlib.Path(__file__).parent

# Une la ruta actual con la subcarpeta y el archivo
archivo_ruta = carpeta_actual / "archivos"

# Lee el contenido de la carpeta y filtra los archivos con extensión .json
contenido = os.listdir(archivo_ruta)

for archivo in contenido:
    try:
        if not archivo.endswith(".json"):
            raise ValueError("Solo se aceptan archivos con extension .json")

    except ValueError as error_extension:
        print(f"Error de Formato: {error_extension}")
        continue  # Continúa con el siguiente archivo

    else:
        ruta = archivo_ruta / archivo
        with open(ruta, "r", encoding="utf-8") as archivo_json:
            datos = json.load(archivo_json)
            resultado = filtroalumnos(list(datos))
            for alumno in resultado:
                if alumno.get("grupo") == "A":
                    print(
                        f"El alumno {alumno.get('nombre')} tiene un promedio de {alumno.get('promedio')} y pertenece al grupo A"
                    )
                if alumno.get("grupo") == "B":
                    print(
                        f"El alumno {alumno.get('nombre')} tiene un promedio de {alumno.get('promedio')} y pertenece al grupo B"
                    )
                if alumno.get("grupo") == "C":
                    print(
                        f"El alumno {alumno.get('nombre')} tiene un promedio de {alumno.get('promedio')} y pertenece al grupo C"
                    )
