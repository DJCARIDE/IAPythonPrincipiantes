import tkinter as tk
from tkinter import ttk

# Craemos una ventana
ventana = tk.Tk()
ventana.geometry('600x400')
ventana.title('Manejo de etiquetas')
ventana.configure(background='#1d2d44')

# Creamos una etiqueta (label)
etiqueta = tk.Label(ventana, text='Saludos')
#etiqueta = tk.Label(ventana, text='Saludos', font=('Arial', 20), bg='#1d2d44', fg='white')
#etiqueta = ttk.Label(ventana, text='Saludos')

# Cambiar el texto usando el metodo configure
#etiqueta.configure(text='Nos vemos...')

# Cambiar el texto con ayuda de la llave text
#etiqueta['text'] = 'Adios'

# Publicamos el componente
#etiqueta.pack()
#etiqueta.pack(pady=20)

ventana.mainloop()