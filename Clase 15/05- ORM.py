from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración de la base de datos
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:admin@localhost/escuela')

# 2. Definición de la clase (mapeo a la tabla 'estudiantes')
class Estudiante(Base):
    __tablename__ = 'estudiantes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    edad = Column(Integer)
    curso = Column(String(50))

    def __repr__(self):
        return f"<Estudiante(id={self.id}, nombre='{self.nombre}', edad={self.edad}, curso='{self.curso}')>"

# 3. Crear la tabla en la base de datos
Base.metadata.create_all(engine)

# 4. Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 5. Insertar datos
estudiante1 = Estudiante(id=12, nombre='Francisco', edad=20, curso='Matemáticas')
estudiante2 = Estudiante(id=22, nombre='Pedro', edad=25, curso='Historia')
estudiante3 = Estudiante(id=32, nombre='Maria Ines', edad=21, curso='Física')
session.add_all([estudiante1, estudiante2, estudiante3])
session.commit()

# 6. Consultar
print("\n--- Estudiantes actuales ---")
for estudiante in session.query(Estudiante).all():
    print(estudiante)

# 7. Actualizar y eliminar
pedro = session.query(Estudiante).filter_by(nombre='Pedro').first()
pedro.curso = 'Literatura'
session.commit()

alumno = session.query(Estudiante).filter_by(id=12).first()
session.delete(alumno)
session.commit()

# 8. Funciones agregadas
print("\n--- Estudiantes después de actualizar y eliminar ---")
for estudiante in session.query(Estudiante).all():
    print(estudiante)

cantidad = session.query(Estudiante).count()
print("\nCantidad:", cantidad)

from sqlalchemy.sql import func
edad_promedio = session.query(func.avg(Estudiante.edad)).scalar()
print("Edad promedio:", edad_promedio)

# 9. Cerrar la sesión
session.close()