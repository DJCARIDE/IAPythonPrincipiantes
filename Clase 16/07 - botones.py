import tkinter as tk
from tkinter import ttk

# Craemos una ventana
ventana = tk.Tk()
ventana.geometry('600x400')
ventana.title('Prueba de Botones')
ventana.configure(background='#1d2d44')


# def saludar():
#     print('Saludos luego del click')

# def saludar(nombre):
#     print(f'Saludos {nombre}')

# Botones
# boton1 = ttk.Button(ventana, text='enviar', command=saludar())
# boton1 = ttk.Button(ventana, text='Enviar', command=lambda: saludar('Omar'))
# boton1.pack(pady=20)


ventana.mainloop()