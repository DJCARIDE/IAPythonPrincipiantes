from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para los mensajes flash

# Inicializar la base de datos
with app.app_context():
    init_db()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    return render_template('clientes/listar_clientes.html', clientes=clientes)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        
        if not nombre or not email or not telefono:
            flash('Todos los campos son requeridos', 'error')
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)',
                (nombre, email, telefono)
            )
            db.commit()
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('index'))
            
    return render_template('clientes/crear_cliente.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        
        if not nombre or not email or not telefono:
            flash('Todos los campos son requeridos', 'error')
        else:
            cursor.execute(
                'UPDATE clientes SET nombre = ?, email = ?, telefono = ? WHERE id = ?',
                (nombre, email, telefono, id)
            )
            db.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cursor.fetchone()
    return render_template('clientes/editar_cliente.html', cliente=cliente)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    db.commit()
    flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)