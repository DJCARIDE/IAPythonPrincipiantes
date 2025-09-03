# Convierte de Programación estructurada a POO
# Transforma este código en un conjunto de clases 
# (Triangulo y Rectángulo) que tengan métodos para calcular su área.
class Triangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return (self.base * self.altura) / 2

class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

# Crear isntancias de Triangulo y Rectangulo
Triangulo = Triangulo(5, 8)
area_triangulo = float(Triangulo.calcular_area ()) 
print(f"Área del triángulo: {area_triangulo}")

Rectangulo = Rectangulo(6, 4)   
area_rectangulo = float(Rectangulo.calcular_area())
print(f"Área del rectángulo: {area_rectangulo}")        

