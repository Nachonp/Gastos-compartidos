import cv2
import pytesseract
import sqlite3
import re
import os
import shutil

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def solicitar_nombre_archivo():
    """Solicita al usuario el nombre del archivo de imagen y verifica si existe."""
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo .jpg (incluyendo la extensión): ").strip()
        ruta_completa = os.path.join(r'D:\Python\Gastos compartidos', nombre_archivo)

        if os.path.exists(ruta_completa):
            return ruta_completa
        else:
            print("Error: Archivo no encontrado. Verifique el nombre y la ubicación.")

def extraer_texto_de_imagen(ruta_imagen):
    """Extrae el texto de una imagen utilizando OCR"""
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("Error: No se pudo cargar la imagen.")
        exit()
    
    texto = pytesseract.image_to_string(imagen)
    return texto

def guardar_texto_bruto(texto, ruta_txt):
    """Guarda el texto extraído en un archivo .txt"""
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

def procesar_texto(texto):
    """Extrae cantidad, productos y precios del texto usando expresiones regulares"""
    productos_precios = []
    lineas = texto.split("\n")
    for linea in lineas:
        match = re.match(r"(\d+)\s+(.+?)\s+\$?(\d+[\.,]?\d*)", linea)
        if match:
            cantidad = int(match.group(1))
            producto = match.group(2).strip()
            precio = float(match.group(3).replace(",", "."))  # Asegurar formato de número
            productos_precios.append((cantidad, producto, precio))
    return productos_precios

def guardar_en_txt(datos, ruta_txt):
    """Guarda la cantidad, los productos y los precios en un archivo .txt"""
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        for cantidad, producto, precio in datos:
            archivo.write(f"{cantidad}x {producto} - ${precio:.2f}\n")

def guardar_en_sqlite(datos, nombre_bd="productos.db"):
    """Guarda la cantidad, los productos y los precios en una base de datos SQLite"""
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cantidad INTEGER,
            nombre TEXT,
            precio REAL
        )
    """)
    cursor.executemany("INSERT INTO productos (cantidad, nombre, precio) VALUES (?, ?, ?)", datos)
    conexion.commit()
    conexion.close()

def solicitar_nombres_usuarios():
    """Solicita el número de personas y sus nombres."""
    while True:
        try:
            num_personas = int(input("Ingrese el número de personas que comparten la compra: "))
            if num_personas <= 0:
                print("Debe haber al menos una persona.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")

    nombres = []
    for i in range(num_personas):
        nombre = input(f"Ingrese el nombre de la persona {i+1}: ").strip()
        nombres.append(nombre)

    return num_personas, nombres

def calcular_gastos_compartidos(datos, num_personas, nombres, ruta_txt):
    """Calcula el total de la compra y divide entre el número de personas, guardando el resultado con nombres."""
    total = sum(cantidad * precio for cantidad, _, precio in datos)
    costo_por_persona = total / num_personas if num_personas > 0 else 0

    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write(f"Total de la compra: ${total:.2f}\n")
        archivo.write(f"Número de personas: {num_personas}\n")
        archivo.write("Gasto por persona:\n")
        for nombre in nombres:
            archivo.write(f"- {nombre}: ${costo_por_persona:.2f}\n")

    print(f"Gasto compartido guardado en {ruta_txt}")

def eliminar_archivos():
    """Elimina archivos generados según la elección del usuario."""
    archivos = ["gastos_compartidos.txt", "productos.txt", "texto_extraido.txt", "productos.db"]
    
    opcion = input("¿Desea eliminar archivos individualmente o todos? (i/t): ").strip().lower()

    if opcion == "t":
        for archivo in archivos:
            if os.path.exists(archivo):
                os.remove(archivo)
                print(f"Eliminado: {archivo}")
    elif opcion == "i":
        for archivo in archivos:
            if os.path.exists(archivo):
                eliminar = input(f"¿Desea eliminar {archivo}? (s/n): ").strip().lower()
                if eliminar == "s":
                    os.remove(archivo)
                    print(f"Eliminado: {archivo}")

def mover_archivos(destino):
    """Mueve los archivos generados a la carpeta especificada"""
    if not os.path.exists(destino):
        os.makedirs(destino)
    archivos = ["gastos_compartidos.txt", "productos.txt", "texto_extraido.txt", "productos.db"]
    for archivo in archivos:
        if os.path.exists(archivo):
            shutil.move(archivo, os.path.join(destino, archivo))
            print(f"Movido: {archivo} a {destino}")

def crear_readme():
    """Crea un archivo readme.txt con todas las extensiones utilizadas en el script"""
    extensiones = [".txt", ".db", ".jpg"]
    with open("readme.txt", "w", encoding="utf-8") as archivo:
        archivo.write("Este script genera los siguientes archivos con sus respectivas extensiones:\n")
        for ext in extensiones:
            archivo.write(f"- Archivos con extensión {ext}\n")

# Uso del script
ruta_imagen = solicitar_nombre_archivo()
texto_extraido = extraer_texto_de_imagen(ruta_imagen)
guardar_texto_bruto(texto_extraido, "texto_extraido.txt")

productos_precios = procesar_texto(texto_extraido)

if productos_precios:
    guardar_en_txt(productos_precios, "productos.txt")
    guardar_en_sqlite(productos_precios)
    
    num_personas, nombres = solicitar_nombres_usuarios()
    calcular_gastos_compartidos(productos_precios, num_personas, nombres, "gastos_compartidos.txt")

    print("Datos extraídos y guardados con éxito. Gasto compartido calculado.")
else:
    print("No se encontraron productos y precios en la imagen.")

# Crear readme.txt
crear_readme()

# Opción para eliminar archivos
if input("¿Desea eliminar los archivos generados? (s/n): ").strip().lower() == "s":
    eliminar_archivos()

# Opción para mover archivos
if input("¿Desea mover los archivos generados a la carpeta de Pruebas? (s/n): ").strip().lower() == "s":
    mover_archivos(r'D:\Python\Gastos compartidos\Pruebas')
