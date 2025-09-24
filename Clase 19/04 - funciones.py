def calcular_area(base, altura):
  """Calcula el área de un rectángulo."""
  return base * altura

# Llamada CORRECTA (la "llave" encaja en la "cerradura"):
area_correcta = calcular_area(10, 5) 
print(f"El área es: {area_correcta}") # Salida: El área es: 50

# Llamada INCORRECTA: le pasamos un tercer argumento
try:
  area_incorrecta = calcular_area(10, 5, 2) # ⚠️ ERROR
except TypeError as e:
  print(f"\nError: {e}")