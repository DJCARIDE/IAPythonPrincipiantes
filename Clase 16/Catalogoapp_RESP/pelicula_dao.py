import sqlite3
from pelicula import Pelicula

class PeliculaDAO:
    def __init__(self, db_name='catalogo.db'):
        self.db_name = db_name

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def inicializar_tabla(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peliculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                director TEXT,
                anio INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def agregar(self, pelicula: Pelicula):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO peliculas (nombre, director, anio)
            VALUES (?, ?, ?)
        ''', (pelicula.nombre, pelicula.director, pelicula.anio))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, director, anio FROM peliculas')
        filas = cursor.fetchall()
        conn.close()
        return [Pelicula(id=f[0], nombre=f[1], director=f[2], anio=f[3]) for f in filas]

    def eliminar(self, id_pelicula):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM peliculas WHERE id = ?', (id_pelicula,))
        conn.commit()
        conn.close()
