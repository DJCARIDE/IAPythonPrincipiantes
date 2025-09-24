def saludar(nombre, saludo="Hola"):
  """Saluda a una persona."""
  print(f"{saludo}, {nombre}!")

# No pasamos el segundo argumento, así que usa el valor por defecto "Hola"
saludar("Ana") # Salida: Hola, Ana!

# Aquí sí lo pasamos, por lo que sobreescribe el valor por defecto
saludar("Carlos", "Buenas noches") # Salida: Buenas noches, Carlos!