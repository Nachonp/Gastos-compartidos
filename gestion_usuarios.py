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
    """Asigna usuarios a cada producto comprado."""
    productos_asignados = []
    usuarios_gastos = {usuario: 0 for usuario in nombres.values()}  # Inicializar gastos

    for cantidad, producto, precio in productos:
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

            if num_compradores == num_personas:
                compradores = list(nombres.values())
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

        # Distribuir el costo entre los compradores
        costo_por_usuario = (cantidad * precio) / len(compradores)
        for usuario in compradores:
            usuarios_gastos[usuario] += costo_por_usuario

    return productos_asignados, usuarios_gastos