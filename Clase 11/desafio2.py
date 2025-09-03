# Identifica y corrige los errores en el código proporcionado.
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def obtener_informacion(self):
        print(f"Coche: {self.marca} {self.modelo}")

mi_coche = Coche("Toyota", "Corolla")
mi_coche.obtener_informacion()
