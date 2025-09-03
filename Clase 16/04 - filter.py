# Supongamos que tienes una lista de números y quieres obtener solo los pares.

numeros = [10, 11, 12, 13, 14, 15]

# La lambda devuelve True si el número es par, y filter() lo conserva.
pares = list(filter(lambda x: x % 2 == 0, numeros))

print(pares)
# Salida: [10, 12, 14]