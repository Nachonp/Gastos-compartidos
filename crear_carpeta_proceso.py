import os

def crear_carpeta_proceso():
    """Crea y retorna la ruta base donde se guardarán los archivos del proceso."""
    ruta_base = r'D:\Python\Gastos compartidos\Procesos\TicketsOriginal'  # Ruta fija
    os.makedirs(ruta_base, exist_ok=True)
    return ruta_base