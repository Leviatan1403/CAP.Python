def filtroalumnos(alumnos: list):
    for alumno in alumnos:
        try:
            if alumno.get("promedio") == 0:
                raise ValueError("El promedio no puede ser nulo")
        except ValueError as error_promedio:
            print(f"Error de promedio es cero: {error_promedio}")
        else:
            assigmentgroup(alumno)
    return alumnos


def assigmentgroup(alumno: dict):
    match alumno:
        case {"promedio": a} if a > 8:
            alumno["grupo"] = "A"
        case {"promedio": a} if a < 8 and a > 6:
            alumno["grupo"] = "B"
        case {"promedio": a} if a < 6 and a > 0:
            alumno["grupo"] = "C"
    return alumno
