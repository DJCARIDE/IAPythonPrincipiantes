# Catalogoapp/pelicula.py
class Pelicula:
    def __init__(self, nombre, director=None, anio=None, id=None):
        self.id = id
        self.nombre = nombre
        self.director = director
        self.anio = anio

    def __str__(self):
        return f"Pelicula({self.id}): {self.nombre} - {self.director} ({self.anio})"