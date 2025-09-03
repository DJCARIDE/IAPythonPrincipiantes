# database.py
# Gestiona la conexión y las operaciones CRUD con la base de datos MySQL.

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class DatabaseManager:
    """
    Clase que encapsula toda la lógica de la base de datos.
    Verifica y crea la base de datos y la tabla si no existen.
    """
    def __init__(self, config):
        self.config = config
        self.connection = None
        self._initialize_database()

    def _initialize_database(self):
        """Crea la base de datos y la tabla si no existen."""
        try:
            db = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"]
            )
            cursor = db.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            cursor.close()
            db.close()
            
            self.connect()
            cursor = self.connection.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    telefono VARCHAR(50)
                )
            """)
            self.connection.commit()
            cursor.close()
            print("Base de datos y tabla verificadas/creadas correctamente.")

        except Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo inicializar la base de datos: {e}")

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.connection = mysql.connector.connect(**self.config)
        except Error as e:
            messagebox.showerror("Error de Conexión", f"Error al conectar a MySQL: {e}")
            self.connection = None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada.")

    def fetch_all_clientes(self):
        """Obtiene todos los clientes de la tabla."""
        if not self.connection: return []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, email, telefono FROM clientes ORDER BY nombre")
            records = cursor.fetchall()
            cursor.close()
            return records
        except Error as e:
            messagebox.showerror("Error de Lectura", f"No se pudieron cargar los clientes: {e}")
            return []

    def insert_cliente(self, nombre, email, telefono):
        """Inserta un nuevo cliente."""
        if not self.connection: return False
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, email, telefono))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            messagebox.showerror("Error de Inserción", f"No se pudo agregar el cliente: {e}")
            return False

    def update_cliente(self, client_id, nombre, email, telefono):
        """Actualiza un cliente existente."""
        if not self.connection: return False
        try:
            cursor = self.connection.cursor()
            query = "UPDATE clientes SET nombre = %s, email = %s, telefono = %s WHERE id = %s"
            cursor.execute(query, (nombre, email, telefono, client_id))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            messagebox.showerror("Error de Actualización", f"No se pudo actualizar el cliente: {e}")
            return False

    def delete_cliente(self, client_id):
        """Elimina un cliente."""
        if not self.connection: return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM clientes WHERE id = %s"
            cursor.execute(query, (client_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            messagebox.showerror("Error de Eliminación", f"No se pudo eliminar el cliente: {e}")
            return False