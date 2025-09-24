def describir_mascota(tipo_animal, nombre):
  """Muestra información de una mascota."""
  print(f"Tengo un {tipo_animal} que se llama {nombre}.")

# El orden de los argumentos de palabra clave no altera el resultado
describir_mascota(nombre="Willy", tipo_animal="perro")
# Salida: Tengo un perro que se llama Willy.

describir_mascota(tipo_animal="gato", nombre="Mishi")
# Salida: Tengo un gato que se llama Mishi.