def generador_por_lotes(iterable, tamano_lote):
    """
    Agrupa un iterable en lotes (chunks) del tamaño especificado.
    """
    lote = []
    for item in iterable:
        lote.append(item)
        if len(lote) == tamano_lote:
            yield lote
            lote = []
    if lote:  # Procesar cualquier elemento restante
        yield lote


# Ejemplo de uso procesando lotes de 3 elementos:
datos = range(1, 11)
for lote in generador_por_lotes(datos, tamano_lote=3):
    print(f"Procesando lote: {lote}")
