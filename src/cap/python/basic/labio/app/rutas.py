from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "datos"
LOG_DIR = BASE_DIR / "logs"

CSV_FILE = DATA_DIR / "ventas.csv"
OUTPUT_FILE = DATA_DIR / "reporte.json"


def validar_rutas() -> None:

    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)

    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True)

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {CSV_FILE}")
