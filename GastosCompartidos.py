import pytesseract
import cv2
import re
import pandas as pd
from PIL import Image

# Configurar la ruta de Tesseract si es necesario
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para preprocesar la imagen y extraer texto
def extraer_texto_ticket(ruta_imagen):
    # Leer la imagen
    imagen = cv2.imread(ruta_imagen)

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral para mejorar el contraste
    _, umbral = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)

    # Extraer texto usando pytesseract
    texto = pytesseract.image_to_string(umbral, lang='spa')
    return texto

# Función para extraer productos y precios usando expresiones regulares
def extraer_productos_precios(texto):
    # Patrón que busca líneas con formato: NombreProducto  Precio
    patron = r'([A-Za-z\s]+)\s+(\d+,\d{2})€'
    coincidencias = re.findall(patron, texto)

    # Convertir a un diccionario
    productos_precios = {producto.strip(): precio for producto, precio in coincidencias}
    return productos_precios

# Ruta de la imagen del ticket
ruta_ticket = r'D:\Python\Gastos compartidos\ticket.jpg'

# Extraer texto del ticket
texto_ticket = extraer_texto_ticket(ruta_ticket)
print("Texto extraído:\n", texto_ticket)

# Extraer productos y precios
productos_precios = extraer_productos_precios(texto_ticket)
print("\nProductos y precios encontrados:")
for producto, precio in productos_precios.items():
    print(f"{producto}: {precio}€")

# Convertir el diccionario a un DataFrame de pandas
df = pd.DataFrame(list(productos_precios.items()), columns=['Producto', 'Precio'])

# Exportar los datos a un archivo .txt
ruta_salida_txt = r'D:\Python\Gastos compartidos\ticket.txt'
with open(ruta_salida_txt, 'w', encoding='utf-8') as archivo:
    # Escribir el texto extraído en el archivo
    archivo.write("Texto extraído:\n")
    archivo.write(texto_ticket)
    archivo.write("\n\nProductos y precios encontrados:\n")
    for producto, precio in productos_precios.items():
        archivo.write(f"{producto}: {precio}€\n")
print(f"\nDatos exportados a {ruta_salida_txt}")
