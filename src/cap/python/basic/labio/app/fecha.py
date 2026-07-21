from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_HORARIA = ZoneInfo("America/Mexico_City")


def obtener_fecha_actual() -> str:
    """
    Obtiene la fecha actual con zona horaria configurada.
    """

    fecha = datetime.now(ZONA_HORARIA)

    return fecha.isoformat()
