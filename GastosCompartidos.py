import cv2
import pytesseract
import os
import re
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db, init_db
from sqlalchemy import Enum



class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ruta_actual = os.path.dirname(__file__)

def solicitar_nombre_archivo():
    """Solicita al usuario el nombre del archivo de imagen y verifica si existe."""
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo .jpg (incluyendo la extensión): ").strip()
        ruta_completa = os.path.join(ruta_actual, nombre_archivo)
        if os.path.isfile(ruta_completa):
            return ruta_completa
        print("Error: Archivo no encontrado. Verifique el nombre y la ubicación.")

def extraer_texto_de_imagen(ruta_imagen):
    """Extrae el texto de una imagen utilizando OCR"""
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("Error: No se pudo cargar la imagen. Verifique el archivo.")
        sys.exit(1)

    return pytesseract.image_to_string(imagen).strip()

def crear_carpeta_proceso():
    """Retorna la ruta base donde se guardarán los archivos del proceso."""
    return ruta_actual + '\Procesos\TicketsOriginal'

def guardar_texto_bruto(texto, ruta_txt):
    """Guarda el texto extraído en un archivo .txt"""
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
            archivo.write(texto)
    
def procesar_texto(texto):
    """Extrae cantidad, productos y precios del texto usando expresiones regulares mejoradas"""
    productos_precios = []
    lineas = texto.split("\n")

    for linea in lineas:
        # Expresión mejorada: captura cantidad, producto y precio sin importar espacios
        match = re.match(r"^\s*(\d+)\s+(.+?)\s+(\d+[\.,]?\d*)\s*$", linea)
        
        if match:
            cantidad = int(match.group(1))  # Columna 1: Cantidad
            producto = match.group(2).strip()  # Columna intermedia: Producto
            precio = float(match.group(3).replace(",", "."))  # Última columna: Precio
            productos_precios.append((cantidad, producto, precio))

    return productos_precios

def solicitar_nombres_usuarios():
    """Solicita el número de personas y sus nombres, asignándoles un número."""
    while True:
        try:
            num_personas = int(input("Ingrese el número de personas que comparten la compra: "))
            if num_personas > 0:
                break
            print("Debe haber al menos una persona.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

    return {i: input(f"Ingrese el nombre de la persona {i}: ").strip() for i in range(1, num_personas + 1)}, num_personas

def asignar_usuarios_a_productos(productos, nombres, num_personas):
    """Asigna usuarios a cada producto comprado, optimizando cuando hay un solo usuario o todos compraron el producto."""
    productos_asignados = []
    usuarios_gastos = {usuario: 0 for usuario in nombres.values()}  # Inicializar gastos

    for cantidad, producto, precio in productos:
        # Si hay solo un usuario, se le asigna todo sin preguntar nada
        if num_personas == 1:
            compradores = list(nombres.values())  # Asigna al único usuario
        else:
            while True:
                try:
                    num_compradores = int(input(f"¿Cuántos usuarios compraron {producto}? "))
                    if 1 <= num_compradores <= num_personas:
                        break
                    print(f"Ingrese un número entre 1 y {num_personas}.")
                except ValueError:
                    print("Ingrese un número válido.")

            # Si todos los usuarios compraron el producto, no se pregunta quiénes fueron
            if num_compradores == num_personas:
                compradores = list(nombres.values())  # Asignar a todos automáticamente
            else:
                compradores = set()
                for _ in range(num_compradores):
                    while True:
                        try:
                            num_usuario = int(input(f"Ingrese el número del usuario que compró {producto}: "))
                            if num_usuario in nombres:
                                compradores.add(nombres[num_usuario])
                                break
                            print("Número de usuario inválido. Intente de nuevo.")
                        except ValueError:
                            print("Ingrese un número válido.")
                compradores = list(compradores)

        productos_asignados.append((cantidad, producto, precio, compradores))

        # Distribuir el costo equitativamente entre los compradores
        costo_por_usuario = (cantidad * precio) / len(compradores)
        for usuario in compradores:
            usuarios_gastos[usuario] += costo_por_usuario

    return productos_asignados, usuarios_gastos

import os

def guardar_resumen(productos_asignados, usuarios_gastos, nombre_archivo):
    """Guarda el resumen de la compra en un archivo .txt, permitiendo renombrar si ya existe."""
    ruta_base = ruta_actual + '\Procesos\Tickets' #yo evitaría usar el término 'base' en cualquier cosa que no sea verdaderamente base de algo
    #una alternativa mejor: ruta_base = ruta_actual + '\Procesos\Tickets'
    ruta_txt = os.path.join(ruta_base, f"{nombre_archivo}.txt")

    while os.path.exists(ruta_txt):
        print(f"⚠️ El archivo '{nombre_archivo}.txt' ya existe.")
        opcion = input("¿Desea sobrescribir (S) o ingresar un nuevo nombre (N)? ").strip().lower()
        if opcion == 's':
            break
        elif opcion == 'n':
            nombre_archivo = input("Ingrese un nuevo nombre para el archivo TXT: ").strip()
            ruta_txt = os.path.join(ruta_base, f"{nombre_archivo}.txt")
        else:
            print("❌ Opción no válida. Intente nuevamente.")

    try:
        with open(ruta_txt, "w", encoding="utf-8") as archivo:
            archivo.write("Resumen de la compra:\n")
            
            for cantidad, producto, precio, compradores in productos_asignados:
                new_ticket = Ticket(person=compradores[0], total_amount=precio)
                db.session.add(new_ticket)
                db.session.commit()
                archivo.write(f"{cantidad}x {producto} - ${precio:.2f} (Comprado por: {', '.join(compradores)})\n")
            archivo.write("\nTotal a pagar por usuario:\n")
            for usuario, gasto in usuarios_gastos.items():
                archivo.write(f"{usuario}: ${gasto:.2f}\n")
        print(f"✅ Archivo guardado exitosamente en: {ruta_txt}")
    except IOError as e:
        print(f"❌ Error al guardar el archivo de resumen: {e}")

#Este método hace falta para envolver la app
def create_app():
    app = Flask(__name__) # Como en NotePoquet, para registrarla en el app_contextrun (creo que se llama)
    with app.app_context(): # "Abrimos" el contexto en que se va a mover la app, para que flask y sqlalchemy funcionen
        init_db(app) # Iniciamos la base de datos
        while True: # Al estar el bucle "principal" de la app dentro del bloque abierto por el contexto, las llamadas a BD funcionan
            # Permite procesar múltiples tickets
            carpeta_proceso = crear_carpeta_proceso()
            nombres_usuarios, num_personas = solicitar_nombres_usuarios()
            ruta_imagen = solicitar_nombre_archivo()
            texto_extraido = extraer_texto_de_imagen(ruta_imagen)

            # Solicitar el nombre del archivo de resumen
            nombre_archivo = input("Ingrese el nombre del archivo TXT de resumen (sin extensión): ").strip()
            # Guardar texto extraído con el nombre basado en el resumen
            ruta_txt = os.path.join(carpeta_proceso, f"t_e_{nombre_archivo}.txt")
            guardar_texto_bruto(texto_extraido, ruta_txt)

            productos_precios = procesar_texto(texto_extraido)
            if productos_precios:
                productos_asignados, usuarios_gastos = asignar_usuarios_a_productos(productos_precios, nombres_usuarios, num_personas)
                guardar_resumen(productos_asignados, usuarios_gastos, nombre_archivo)  # Pasar el nombre del archivo
            else:
                print("❌ No se encontraron productos y precios en la imagen.")

            # Opción para procesar otro ticket
            reiniciar = input("\n¿Desea procesar otro ticket? (S/N): ").strip().lower()
            if reiniciar != 's':
                print("👋 ¡Gracias por usar el programa!")
                break  # Sale del bucle y finaliza el programa
#def main():

if __name__ == "__main__":
    create_app()
    #main()
    