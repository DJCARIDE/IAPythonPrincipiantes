def sumar(*args):
    """Suma todos los números pasados como argumentos."""
    total = 0
    # args es una tupla, por lo que podemos iterar sobre ella
    for numero in args:
        total += numero
    return total

# Probemos la función con diferentes cantidades de argumentos
print(sumar(5, 10))          # Salida: 15
print(sumar(1, 2, 3, 4, 5))  # Salida: 15
print(sumar(100, -50, 25))   # Salida: 75