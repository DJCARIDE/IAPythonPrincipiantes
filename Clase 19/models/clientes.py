import sqlite3
from typing import Optional, List

from database import get_db


class Clientes:
    """Capa de acceso a datos para la tabla clientes."""

    @staticmethod
    def listar_todos() -> List[sqlite3.Row]:
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM clientes ORDER BY id DESC')
        return cur.fetchall()

    @staticmethod
    def obtener_por_id(cliente_id: int) -> Optional[sqlite3.Row]:
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        return cur.fetchone()

    @staticmethod
    def crear(nombre: str, email: str, telefono: str) -> int:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)',
            (nombre, email, telefono)
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def actualizar(cliente_id: int, nombre: str, email: str, telefono: str) -> int:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'UPDATE clientes SET nombre = ?, email = ?, telefono = ? WHERE id = ?',
            (nombre, email, telefono, cliente_id)
        )
        db.commit()
        return cur.rowcount

    @staticmethod
    def eliminar(cliente_id: int) -> int:
        db = get_db()
        cur = db.cursor()
        cur.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        db.commit()
        return cur.rowcount
