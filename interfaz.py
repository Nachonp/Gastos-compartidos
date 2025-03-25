import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from ocr_extraccion import extraer_texto_de_imagen
from procesamiento_texto import procesar_texto
from gestion_usuarios import asignar_usuarios_a_productos
from guardar_archivos import guardar_resumen


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

    nombres_usuarios = {i: input(f"Ingrese el nombre de la persona {i}: ").strip() for i in range(1, num_personas + 1)}
    return nombres_usuarios, num_personas


def cargar_archivo():
    """Permite cargar un archivo de imagen desde el explorador de archivos."""
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if ruta_archivo:
        archivo_entry.delete(0, tk.END)
        archivo_entry.insert(0, ruta_archivo)


def procesar_ticket():
    """Procesa el ticket cargado y muestra el resumen."""
    ruta_imagen = archivo_entry.get().strip()

    if not ruta_imagen:
        messagebox.showerror("Error", "Debe cargar un archivo de imagen.")
        return

    # Solicitar nombres de usuarios y número de personas
    nombres_usuarios, num_personas = solicitar_nombres_usuarios()

    # Aquí, puedes llamar a las funciones correspondientes para extraer el texto y procesarlo
    texto_extraido = extraer_texto_de_imagen(ruta_imagen)
    productos_precios = procesar_texto(texto_extraido)

    if productos_precios:
        productos_asignados, usuarios_gastos = asignar_usuarios_a_productos(productos_precios, nombres_usuarios, num_personas)
        resumen = generar_resumen(productos_asignados, usuarios_gastos)
        mostrar_resumen(resumen)
    else:
        messagebox.showerror("Error", "No se encontraron productos y precios en la imagen.")


def generar_resumen(productos_asignados, usuarios_gastos):
    """Genera el resumen de la compra."""
    resumen = "Resumen de la compra:\n"
    for cantidad, producto, precio, compradores in productos_asignados:
        resumen += f"{cantidad}x {producto} - ${precio:.2f} (Comprado por: {', '.join(compradores)})\n"
    resumen += "\nTotal a pagar por usuario:\n"
    for usuario, gasto in usuarios_gastos.items():
        resumen += f"{usuario}: ${gasto:.2f}\n"
    return resumen


def mostrar_resumen(resumen_texto):
    """Crea una ventana para mostrar el resumen con scroll"""
    ventana_resumen = tk.Toplevel()  # Crea una nueva ventana
    ventana_resumen.title("Resumen de la Compra")
    
    # Configurar la opción de redimensionar
    ventana_resumen.geometry("500x400")
    ventana_resumen.resizable(True, True)  # Permitir redimensionar la ventana
    
    # Crear un frame que contenga el Text Widget y el Scrollbar
    frame_resumen = tk.Frame(ventana_resumen)
    frame_resumen.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Crear un Canvas para permitir que el contenido sea desplazable
    canvas = tk.Canvas(frame_resumen)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Crear el Scrollbar
    scrollbar = tk.Scrollbar(frame_resumen, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Crear un Frame dentro del Canvas que contendrá el Text widget
    frame_texto = tk.Frame(canvas)
    
    # Crear el Text Widget
    texto_resumen = tk.Text(frame_texto, wrap=tk.WORD, height=15, width=60)
    texto_resumen.insert(tk.END, resumen_texto)
    texto_resumen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configurar el Scrollbar para controlar el canvas
    canvas.create_window((0, 0), window=frame_texto, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Actualizar el área del canvas para ajustarse al tamaño del texto
    frame_texto.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Crear algunos botones dentro de la ventana que se redimensionen
    boton_aceptar = tk.Button(ventana_resumen, text="Aceptar", command=ventana_resumen.destroy)
    boton_aceptar.pack(fill=tk.X, padx=10, pady=5)  # Se adapta al ancho de la ventana
    
    # Ejecutar la ventana
    ventana_resumen.mainloop()


# Configurar la ventana principal
ventana = tk.Tk()
ventana.title("Procesador de Tickets")

# Crear los elementos de la interfaz
archivo_label = tk.Label(ventana, text="Cargar archivo de imagen:")
archivo_label.grid(row=0, column=0, padx=10, pady=10)

archivo_entry = tk.Entry(ventana, width=50)
archivo_entry.grid(row=0, column=1, padx=10, pady=10)

cargar_button = tk.Button(ventana, text="Cargar", command=cargar_archivo)
cargar_button.grid(row=0, column=2, padx=10, pady=10)

procesar_button = tk.Button(ventana, text="Procesar Ticket", command=procesar_ticket)
procesar_button.grid(row=1, column=1, padx=10, pady=10)

# Ejecutar la ventana principal
ventana.mainloop()
