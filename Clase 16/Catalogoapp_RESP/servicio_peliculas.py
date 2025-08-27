# Catalogoapp/servicio_peliculas.py
from pelicula import Pelicula
from pelicula_dao import PeliculaDAO

class ServicioPeliculas:
    def __init__(self):
        self.dao = PeliculaDAO()
        self.dao.inicializar_tabla()

    def agregar_pelicula(self, pelicula):
        self.dao.agregar(pelicula)
        print(f"Película '{pelicula.nombre}' agregada correctamente.")

    def listar_peliculas(self):
        peliculas = self.dao.listar()
        print("--- Listado de películas: ---")
        for pelicula in peliculas:
            print(pelicula)
        print("--- Fin del listado ---\n")

    def eliminar_catalogo(self):
        # Elimina todas las películas de la tabla
        from sqlite3 import connect
        conn = connect(self.dao.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM peliculas")
        conn.commit()
        conn.close()
        print("Catálogo de películas eliminado.")
