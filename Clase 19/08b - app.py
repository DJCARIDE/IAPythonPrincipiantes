from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    # Datos que queremos pasar a la plantilla
    titulo = "Mi increíble página con Flask"
    usuario = "Alex"
    lista_de_tareas = ["Comprar leche", "Aprender Flask", "Dominar el mundo"]

    # render_template busca 'index.html' en la carpeta 'templates'
    # y le pasa las variables
    return render_template(
        'tareas.html', 
        titulo_de_pagina=titulo, 
        nombre_usuario=usuario,
        tareas=lista_de_tareas
    )

if __name__ == '__main__':
    app.run(debug=True)