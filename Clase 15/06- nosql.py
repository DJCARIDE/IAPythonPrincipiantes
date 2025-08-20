# Importamos el cliente de MongoDB
from pymongo import MongoClient

# Conectarse al servidor de MongoDB
client = MongoClient('mongodb://localhost:27017/')  # La URL depende de tu configuración

# Seleccionar la base de datos (se creará automáticamente si no existe)
db = client['mi_empresa']

# Seleccionar la colección (se creará automáticamente si no existe)
empleados = db['empleados']

# Crear un documento JSON (donde se almacena la información de un empleado)
nuevo_empleado = {
    "nombre": "Ana López",
    "puesto": "Analista de Datos",
    "edad": 30,
    "skills": ["Python", "SQL", "Estadística"]
}

# Insertar el documento en la colección
empleado_id = empleados.insert_one(nuevo_empleado).inserted_id
print(f"Empleado insertado con ID: {empleado_id}")

# Crear un documento JSON (donde se almacena la información de un empleado)
nuevo_empleado = {
    "nombre": "Jose Perez",
    "puesto": "Desarrollador Python",
    "edad": 28,
    "skills": ["Python", "SQL"]
}

# Insertar el documento en la colección
empleado_id = empleados.insert_one(nuevo_empleado).inserted_id
print(f"Empleado insertado con ID: {empleado_id}")

# Buscar el documento insertado
#empleado = empleados.find_one({"nombre": "Ana López"})
#print("Documento encontrado:", empleado)