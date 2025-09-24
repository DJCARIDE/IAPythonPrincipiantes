from flask import Flask, render_template

app = Flask(__name__)

app_titulo = 'Mi blog'
usuario = {
    'nombre': 'Juan',
    'email': 'juan@example.com'
}

@app.route('/')  # url: http://localhost:5000/
def index():
    app.logger.debug('Entramos al path de inicio /')
    return render_template('inicio2.html', titulo=app_titulo)

@app.route('/perfil')  # url: http://localhost:5000/perfil
def perfil():
    app.logger.debug('Entramos al path de perfil /')
    return render_template('perfil.html', titulo=app_titulo, usuario=usuario)


if __name__ == '__main__':
    app.run(debug=True)