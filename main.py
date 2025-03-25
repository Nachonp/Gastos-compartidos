from solicitar_archivo import solicitar_nombre_archivo
from ocr_extraccion import extraer_texto_de_imagen
from procesamiento_texto import procesar_texto
from gestion_usuarios import asignar_usuarios_a_productos
from guardar_archivos import crear_carpeta_proceso, guardar_texto_bruto, guardar_resumen
from interfaz import cargar_archivo, procesar_ticket, generar_resumen, mostrar_resumen
import os
import tkinter as tk
from tkinter import simpledialog

def ingresar_datos_usuario():
    """Función para ingresar datos de los usuarios en la interfaz."""
    # Crear una ventana de diálogo para ingresar el número de personas
    num_personas = simpledialog.askinteger("Número de Personas", "Ingrese el número de personas que comparten la compra:", minvalue=1)
    if not num_personas:
        return {}, 0

    # Crear un diccionario para los nombres de los usuarios
    nombres_usuarios = {}
    for i in range(1, num_personas + 1):
        nombre = simpledialog.askstring("Nombre de Usuario", f"Ingrese el nombre de la persona {i}:")
        if nombre:
            nombres_usuarios[i] = nombre.strip()

    return nombres_usuarios, num_personas


def main():
    while True:
        # Crear carpeta base
        carpeta_proceso = crear_carpeta_proceso()
        
        # Solicitar nombres de usuarios desde la interfaz
        nombres_usuarios, num_personas = ingresar_datos_usuario()
        if num_personas == 0:
            break

        # Solicitar ruta de la imagen desde la interfaz
        ruta_imagen = solicitar_nombre_archivo()

        # Extraer texto de la imagen
        texto_extraido = extraer_texto_de_imagen(ruta_imagen)

        # Solicitar el nombre del archivo de resumen
        nombre_archivo = simpledialog.askstring("Nombre del Archivo", "Ingrese el nombre del archivo TXT de resumen (sin extensión):").strip()

        # Guardar el texto extraído
        ruta_txt = os.path.join(carpeta_proceso, f"t_e_{nombre_archivo}.txt")
        guardar_texto_bruto(texto_extraido, ruta_txt)

        # Procesar el texto extraído
        productos_precios = procesar_texto(texto_extraido)

        # Si hay productos válidos, continuar con la asignación de gastos
        if productos_precios:
            productos_asignados, usuarios_gastos = asignar_usuarios_a_productos(productos_precios, nombres_usuarios, num_personas)
            guardar_resumen(productos_asignados, usuarios_gastos, nombre_archivo)
            
            # Generar y mostrar el resumen
            resumen = generar_resumen(productos_asignados, usuarios_gastos)
            mostrar_resumen(resumen)
        else:
            print("❌ No se encontraron productos y precios en la imagen.")

        # Opción para procesar otro ticket
        reiniciar = simpledialog.askstring("Procesar Otro Ticket", "¿Desea procesar otro ticket? (S/N):").strip().lower()
        if reiniciar != 's':
            print("👋 ¡Gracias por usar el programa!")
            break


if __name__ == "__main__":
    main()
