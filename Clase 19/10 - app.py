from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def cargar_clientes():
    try:
        with open('clientes.json', 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"clientes": []}

@app.route('/')
def index():
    return render_template('clientes.html')

@app.route('/api/clientes')
def get_clientes():
    datos = cargar_clientes()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)