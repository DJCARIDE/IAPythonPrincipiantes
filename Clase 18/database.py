import sqlite3
import os
from flask import g

DATABASE = 'clientes.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())
    
    # Verificar si la tabla está vacía
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM clientes')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insertar algunos datos de ejemplo
        cursor.executescript('''
            INSERT INTO clientes (nombre, email, telefono) VALUES
            ('Juan Pérez', 'juan@email.com', '555-0001'),
            ('María García', 'maria@email.com', '555-0002'),
            ('Carlos López', 'carlos@email.com', '555-0003');
        ''')
        db.commit()