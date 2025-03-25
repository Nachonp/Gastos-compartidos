def guardar_texto_bruto(texto, ruta_txt):
    """Guarda el texto extraído en un archivo .txt."""
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
