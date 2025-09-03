import tkinter as tk
from tkinter import ttk, messagebox
import json

def crear_tabla(frame):
    # Crear scrollbar
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear Treeview (tabla)
    tabla = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
    tabla.pack(fill=tk.BOTH, expand=True)

    # Configurar scrollbar
    scrollbar.config(command=tabla.yview)

    # Definir columnas
    tabla['columns'] = ('ID', 'Nombre', 'Email', 'Teléfono')

    # Formatear columnas
    tabla.column('#0', width=0, stretch=tk.NO)
    tabla.column('ID', anchor=tk.CENTER, width=50)
    tabla.column('Nombre', anchor=tk.W, width=200)
    tabla.column('Email', anchor=tk.W, width=200)
    tabla.column('Teléfono', anchor=tk.W, width=100)

    # Crear encabezados
    tabla.heading('#0', text='', anchor=tk.CENTER)
    tabla.heading('ID', text='ID', anchor=tk.CENTER)
    tabla.heading('Nombre', text='Nombre', anchor=tk.CENTER)
    tabla.heading('Email', text='Email', anchor=tk.CENTER)
    tabla.heading('Teléfono', text='Teléfono', anchor=tk.CENTER)

    # Crear estilos
    estilo = ttk.Style()
    estilo.configure('Treeview.Heading', font=('Arial', 16, 'bold'))
    estilo.configure('Treeview', font=('Arial', 12))


    # Agregar el evento de clic
    tabla.bind('<<TreeviewSelect>>', mostrar_datos_cliente)
    
    return tabla

def mostrar_datos_cliente(event):
    # Obtener el item seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    
    # Obtener los valores del item seleccionado
    item = tabla.item(seleccion[0])
    valores = item['values']
    
    # Crear mensaje con los datos del cliente
    mensaje = f"""Datos del Cliente:
ID: {valores[0]}
Nombre: {valores[1]}
Email: {valores[2]}
Teléfono: {valores[3]}"""
    
    # Mostrar messagebox con los datos
    messagebox.showinfo("Información del Cliente", mensaje)

def cargar_datos():
    # Limpiar tabla antes de cargar
    for item in tabla.get_children():
        tabla.delete(item)
        
    try:
        with open('clientes.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            for cliente in datos['clientes']:
                tabla.insert('', tk.END, values=(
                    cliente['id'],
                    cliente['nombre'],
                    cliente['email'],
                    cliente['telefono']
                ))
    except FileNotFoundError:
        print("Error: No se encontró el archivo clientes.json")
    except json.JSONDecodeError:
        print("Error: El archivo JSON no tiene el formato correcto")
    except Exception as e:
        print(f"Error inesperado: {e}")

def limpiar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Visualizador de Clientes")
ventana.geometry("800x600")

# Configurar el grid
ventana.grid_rowconfigure(0, weight=1)  # La fila de la tabla se expandirá
ventana.grid_rowconfigure(1, weight=0)  # La fila de botones no se expandirá
ventana.grid_columnconfigure(0, weight=1)  # La columna se expandirá

# Crear frame para la tabla
frame_tabla = ttk.Frame(ventana, padding="10")
frame_tabla.grid(row=0, column=0, sticky="nsew")

# Crear la tabla dentro del frame
tabla = crear_tabla(frame_tabla)

# Crear frame para los botones
frame_botones = ttk.Frame(ventana, padding="10")
frame_botones.grid(row=1, column=0, sticky="ew")

# Centrar los botones en el frame
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)
frame_botones.grid_columnconfigure(2, weight=1)

# Crear botones
btn_cargar = ttk.Button(frame_botones, text="Cargar", command=cargar_datos)
btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=limpiar_tabla)

# Posicionar botones
btn_cargar.grid(row=0, column=0, padx=5, pady=5, sticky="e")
btn_limpiar.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Iniciar el loop principal
ventana.mainloop()