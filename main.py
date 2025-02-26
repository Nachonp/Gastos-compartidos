import ast

def obtener_librerias(script_file):
    """Escanea un script de Python y devuelve los módulos importados en él."""
    with open(script_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=script_file)

    # Obtener los nombres de los módulos importados
    imported_modules = {alias.name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_modules |= {node.module.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    return sorted(imported_modules)

def guardar_requerimientos(modulos, output_file="requirements.txt"):
    """Guarda la lista de módulos en un archivo de texto."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(modulos))
    print(f"Archivo '{output_file}' creado con éxito.")

if __name__ == "__main__":
    script_file = "GastosCompartidos.py"  # Cambia esto si quieres analizar otro archivo
    modulos = obtener_librerias(script_file)
    
    print("Módulos usados en el script:")
    print("\n".join(modulos))
    
    guardar_requerimientos(modulos)

