from decoradores_lib import mi_decorador


@mi_decorador
def saludar():
    print("¡Hola, mundo!")


if __name__ == "__main__":
    saludar()
