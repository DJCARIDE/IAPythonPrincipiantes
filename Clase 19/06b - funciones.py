def mostrar_info_usuario(**kwargs):
    """Muestra la información de un usuario pasada como argumentos de palabra clave."""
    print("Detalles del usuario:")
    # kwargs es un diccionario, por lo que podemos usar .items() para iterarlo
    for clave, valor in kwargs.items():
        print(f"- {clave.capitalize()}: {valor}")

# Probemos la función
mostrar_info_usuario(nombre="Ana", edad=30, ciudad="Buenos Aires")
print("-" * 20)
mostrar_info_usuario(usuario="juan_perez", email="juan@example.com", activo=True)