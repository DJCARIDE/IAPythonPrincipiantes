# Supongamos que quieres obtener el doble de cada número en una lista.

numeros = [1, 2, 3, 4, 5]

# Usamos lambda para definir la operación "multiplicar por 2" sobre la marcha.
dobles = list(map(lambda x: x * 2, numeros))

print(dobles)
# Salida: [2, 4, 6, 8, 10]