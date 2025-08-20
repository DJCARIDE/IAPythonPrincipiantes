# Catalogoapp/servicio_peliculas.py
import os

class ServicioPeliculas:
    
    def __init__(self):
        self.nombre_archivo = 'catalogo_peliculas.txt'

    def agregar_pelicula(self, pelicula):
        with open(self.nombre_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(f'{pelicula.nombre}\n')

    def listar_peliculas(self):
        with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
            print("--- Listado de películas: ---")
            for linea in archivo:
                print(linea.strip())
            print("--- Fin del listado ---\n")    
    
    def eliminar_archivo(self):        
        if os.path.exists(self.nombre_archivo):
            os.remove(self.nombre_archivo)
            print(f"Archivo {self.nombre_archivo} eliminado.")
        else:
            print(f"El archivo {self.nombre_archivo} no existe.")           
