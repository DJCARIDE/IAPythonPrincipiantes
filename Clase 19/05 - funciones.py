def calcular_area(base, altura):
  return base * altura

# Llamada INCORRECTA: 'ancho' no es un parámetro definido en la firma.
try:
    area_incorrecta = calcular_area(base=10, ancho=5) # ⚠️ ERROR
except TypeError as e:
    print(f"Error: {e}")