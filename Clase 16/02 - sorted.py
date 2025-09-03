# Imagina que tienes una lista de tuplas (nombre, edad) y quieres ordenarla por edad (el segundo elemento).

estudiantes = [('Ana', 25), ('Juan', 21), ('Eva', 29)]

# Usamos lambda para decirle a sorted() que use el segundo elemento (índice 1) como clave de ordenamiento.
ordenados_por_edad = sorted(estudiantes, key=lambda estudiante: estudiante[1])

print(ordenados_por_edad)
# Salida: [('Juan', 21), ('Ana', 25), ('Eva', 29)]