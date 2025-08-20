import mysql.connector

# 1. Conexión inicial sin base de datos para crearla si no existe
try:
    print("[DEBUG] Conectando a MySQL para crear la base de datos si no existe...")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="admin",
        connection_timeout=5
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS escuela")
    conn.commit()
    print("[DEBUG] Base de datos 'escuela' verificada/creada.")
    conn.close()
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudo crear/verificar la base de datos: {err}")
    input("Presiona Enter para salir...")
    exit(1)

# 2. Conexión a la base de datos ya existente
try:
    print("[DEBUG] Iniciando conexión a la base de datos...")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="admin",
        database="escuela",
        connection_timeout=5
    )
    if conn.is_connected():
        print("[DEBUG] Conexión establecida correctamente.")
        try:
            cursor = conn.cursor()
            print("[DEBUG] Cursor creado. Conexión exitosa a la base de datos.")
        except mysql.connector.Error as cursor_err:
            print(f"[ERROR] No se pudo crear el cursor: {cursor_err}")
            input("Presiona Enter para salir...")
            conn.close()
            exit(1)
    else:
        print("[ERROR] No se pudo conectar a la base de datos.")
        input("Presiona Enter para salir...")
        exit(1)
except mysql.connector.Error as err:
    print(f"[ERROR] Fallo la conexión: {err}")
    input("Presiona Enter para salir...")
    exit(1)

# 3. Crear tabla
print("[DEBUG] Creando tabla estudiantes...")
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INT PRIMARY KEY,
        nombre VARCHAR(50),
        edad INT,
        curso VARCHAR(50)
    )
    """)
    print("[DEBUG] Tabla estudiantes creada o ya existe.")
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudo crear la tabla: {err}")
    input("Presiona Enter para salir...")
    conn.close()
    exit(1)

# 4. Insertar datos
print("[DEBUG] Insertando datos en estudiantes...")
try:
    cursor.executemany("""
    INSERT INTO estudiantes (id, nombre, edad, curso)
    VALUES (%s, %s, %s, %s)
    """, [
        (1, 'Ana', 20, 'Matemáticas'),
        (2, 'Juan', 22, 'Historia'),
        (3, 'Maria', 21, 'Física')
    ])
    print("[DEBUG] Datos insertados correctamente.")
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudieron insertar los datos: {err}")
    input("Presiona Enter para salir...")
    conn.close()
    exit(1)

# 5. Consultar
print("[DEBUG] Consultando estudiantes...")
try:
    cursor.execute("SELECT * FROM estudiantes")
    filas = cursor.fetchall()
    print("[DEBUG] Resultados de la consulta:")
    for fila in filas:
        print(fila)
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudo consultar la tabla: {err}")
    input("Presiona Enter para salir...")
    conn.close()
    exit(1)

# 6. Actualizar y eliminar
print("[DEBUG] Actualizando y eliminando registros...")
try:
    cursor.execute("UPDATE estudiantes SET curso = 'Literatura' WHERE nombre = 'Juan'")
    cursor.execute("DELETE FROM estudiantes WHERE id = 3")
    print("[DEBUG] Registros actualizados y eliminados.")
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudieron actualizar/eliminar registros: {err}")
    input("Presiona Enter para salir...")
    conn.close()
    exit(1)

# 7. Funciones agregadas
print("[DEBUG] Ejecutando funciones agregadas...")
try:
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    print("Cantidad:", cursor.fetchone()[0])
    cursor.execute("SELECT AVG(edad) FROM estudiantes")
    print("Edad promedio:", cursor.fetchone()[0])
except mysql.connector.Error as err:
    print(f"[ERROR] No se pudieron ejecutar las funciones agregadas: {err}")
    input("Presiona Enter para salir...")
    conn.close()
    exit(1)

# 8. Confirmar cambios y cerrar conexión
print("[DEBUG] Confirmando cambios y cerrando conexión...")
conn.commit()
conn.close()
print("[DEBUG] Conexión cerrada correctamente.")


