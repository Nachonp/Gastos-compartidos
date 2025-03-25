import os

def crear_carpeta_proceso():
    """Crea y retorna la ruta base donde se guardarán los archivos del proceso."""
    ruta_base = r'D:\Python\Gastos compartidos\Procesos\TicketsOriginal'  # Ruta fija
    os.makedirs(ruta_base, exist_ok=True)
    return ruta_base

def guardar_texto_bruto(texto, ruta_txt):
    """Guarda el texto extraído en un archivo .txt."""
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

def guardar_resumen(productos_asignados, usuarios_gastos, nombre_archivo):
    """Guarda el resumen de la compra en un archivo .txt, permitiendo renombrar si ya existe."""
    ruta_base = r'D:\Python\Gastos compartidos\Procesos\Tickets'
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
                archivo.write(f"{cantidad}x {producto} - ${precio:.2f} (Comprado por: {', '.join(compradores)})\n")
            archivo.write("\nTotal a pagar por usuario:\n")
            for usuario, gasto in usuarios_gastos.items():
                archivo.write(f"{usuario}: ${gasto:.2f}\n")
        print(f"✅ Archivo guardado exitosamente en: {ruta_txt}")
    except IOError as e:
        print(f"❌ Error al guardar el archivo de resumen: {e}")

