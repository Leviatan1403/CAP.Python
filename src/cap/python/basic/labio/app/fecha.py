from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_HORARIA = ZoneInfo("America/Mexico_City")


def obtener_fecha_actual() -> str:

    fecha = datetime.now(ZONA_HORARIA)

    return fecha.isoformat()
