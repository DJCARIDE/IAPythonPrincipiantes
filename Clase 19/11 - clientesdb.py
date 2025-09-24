from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import init_db, close_db
from models.clientes import Clientes

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para los mensajes flash

# Cerrar la base de datos al finalizar la aplicación
# especialmente se se trabaja con multiples workers
app.teardown_appcontext(close_db)

# Inicializar la base de datos
with app.app_context():
    init_db()

@app.route('/')
def index():
    clientes = Clientes.listar_todos()
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
            try:
                Clientes.crear(nombre, email, telefono)
                flash('Cliente creado exitosamente', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('El email ya existe', 'error')
            
    return render_template('clientes/crear_cliente.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        
        if not nombre or not email or not telefono:
            flash('Todos los campos son requeridos', 'error')
        else:
            try:
                updated = Clientes.actualizar(id, nombre, email, telefono)
                if updated == 0:
                    flash('Cliente no encontrado', 'error')
                else:
                    flash('Cliente actualizado exitosamente', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('El email ya existe', 'error')
    
    cliente = Clientes.obtener_por_id(id)
    return render_template('clientes/editar_cliente.html', cliente=cliente)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    deleted = Clientes.eliminar(id)
    if deleted == 0:
        flash('Cliente no encontrado', 'error')
    else:
        flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)