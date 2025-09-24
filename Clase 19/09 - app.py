from flask import Flask, render_template

app = Flask(__name__)

app_titulo = 'Mi primera app con Flask'

@app.route('/')  # url: http://localhost:5000/
@app.route('/inicio')  # url: http://localhost:5000/inicio
def inicio():
    app.logger.debug('Entramos al path de inicio /')
    return render_template('inicio.html', titulo=app_titulo)


@app.route('/page2')  # url: http://localhost:5000/page2
def page2():
    app.logger.debug('Entramos al path page2 /')
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)