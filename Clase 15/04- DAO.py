import mysql.connector

class EstudianteDAO:
    """Clase DAO para gestionar la tabla de estudiantes."""
    
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def _ejecutar_consulta(self, consulta, datos=None):
        """Método auxiliar para ejecutar consultas."""
        cursor = self.conn.cursor()
         # Si 'datos' es una lista, asumimos que es para executemany
        if isinstance(datos, list):
            cursor.executemany(consulta, datos)
            self.conn.commit()
        # Si no, usamos execute (funciona para tuplas o None)
        else:
            cursor.execute(consulta, datos)
            # Solo hacer commit si no es una consulta de selección
            if not consulta.strip().upper().startswith("SELECT"):
                self.conn.commit()
        return cursor

    def crear_tabla(self):
        """Crea la tabla de estudiantes si no existe."""
        self._ejecutar_consulta("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INT PRIMARY KEY,
            nombre VARCHAR(50),
            edad INT,
            curso VARCHAR(50)
        )
        """)
        print("Tabla 'estudiantes' creada o ya existente.")

    def insertar_estudiantes(self, estudiantes):
        """Inserta varios estudiantes en la tabla."""
        consulta = "INSERT INTO estudiantes (id, nombre, edad, curso) VALUES (%s, %s, %s, %s)"
        cursor = self._ejecutar_consulta(consulta, estudiantes)
        print(f"Se insertaron {cursor.rowcount} estudiantes.")

    def obtener_todos_los_estudiantes(self):
        """Obtiene y devuelve todos los estudiantes."""
        cursor = self._ejecutar_consulta("SELECT * FROM estudiantes")
        return cursor.fetchall()

    def actualizar_curso(self, nombre, nuevo_curso):
        """Actualiza el curso de un estudiante por su nombre."""
        consulta = "UPDATE estudiantes SET curso = %s WHERE nombre = %s"
        self._ejecutar_consulta(consulta, (nuevo_curso, nombre))
        print(f"Curso de '{nombre}' actualizado a '{nuevo_curso}'.")

    def eliminar_estudiante(self, id_estudiante):
        """Elimina un estudiante por su ID."""
        consulta = "DELETE FROM estudiantes WHERE id = %s"
        self._ejecutar_consulta(consulta, (id_estudiante,))
        print(f"Estudiante con ID {id_estudiante} eliminado.")

    def obtener_conteo_estudiantes(self):
        """Devuelve la cantidad total de estudiantes."""
        cursor = self._ejecutar_consulta("SELECT COUNT(*) FROM estudiantes")
        return cursor.fetchone()[0]

    def obtener_edad_promedio(self):
        """Devuelve la edad promedio de los estudiantes."""
        cursor = self._ejecutar_consulta("SELECT AVG(edad) FROM estudiantes")
        return cursor.fetchone()[0]

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()
        print("Conexión a la base de datos cerrada.")


# --- Uso del DAO en el programa principal ---
if __name__ == "__main__":
    dao = EstudianteDAO(host="localhost", 
                        user="root", 
                        password="admin", 
                        database="escuela")

    dao.crear_tabla()
    
    estudiantes_a_insertar = [
        (1, 'Ana', 20, 'Matemáticas'),
        (2, 'Juan', 22, 'Historia'),
        (3, 'Maria', 21, 'Física')
    ]
    dao.insertar_estudiantes(estudiantes_a_insertar)
    
    print("\n--- Estudiantes actuales ---")
    estudiantes = dao.obtener_todos_los_estudiantes()
    for est in estudiantes:
        print(est)
    
    dao.actualizar_curso('Juan', 'Literatura')
    dao.eliminar_estudiante(3)

    print("\n--- Estudiantes después de actualizar y eliminar ---")
    estudiantes = dao.obtener_todos_los_estudiantes()
    for est in estudiantes:
        print(est)
        
    print("\nCantidad total de estudiantes:", dao.obtener_conteo_estudiantes())
    print("Edad promedio de estudiantes:", dao.obtener_edad_promedio())
    
    dao.cerrar_conexion()