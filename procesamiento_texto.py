import re


def procesar_texto(texto):
    """Extrae cantidad, productos y precios del texto usando expresiones regulares."""
    productos_precios = []
    lineas = texto.split("\n")

    for linea in lineas:
        # Expresión regular que captura cantidad, producto y precio
        match = re.match(r"^\s*(\d+)\s+(.+?)\s+(\d+[\.,]?\d*)\s*$", linea)

        if match:
            cantidad = int(match.group(1))  # Cantidad
            producto = match.group(2).strip()  # Producto
            precio = float(match.group(3).replace(",", "."))  # Precio
            productos_precios.append((cantidad, producto, precio))

    return productos_precios
