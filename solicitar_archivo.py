import os


def solicitar_nombre_archivo():
    """Solicita al usuario el nombre del archivo de imagen y verifica si existe."""
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo .jpg (incluyendo la extensión): ").strip()
        ruta_completa = os.path.join(r'D:\Python\Gastos compartidos', nombre_archivo)

        if os.path.isfile(ruta_completa):
            return ruta_completa
        print("Error: Archivo no encontrado. Verifique el nombre y la ubicación.")
