import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import USUARIO_CORRECTO, PASSWORD_CORRECTO



def validar_login():
    usuario = entry_usuario.get()
    password = entry_password.get()
    
    if usuario == USUARIO_CORRECTO and password == PASSWORD_CORRECTO:
        messagebox.showinfo("Login exitoso", "Bienvenido, " + usuario)
        ventana.destroy()  # Cierra la ventana de login
        abrir_ventana_principal()  # Abre la ventana principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def abrir_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Ventana Principal")
    ventana_principal.geometry("800x600")

    ttk.Label(ventana_principal, text="Bienvenido al sistema", font=("Arial", 14)).pack(pady=20)
    ttk.Button(ventana_principal, text="Salir", command=ventana_principal.destroy).pack(pady=10)

    ventana_principal.mainloop()

# Crear ventana de login
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("300x200")

ttk.Label(ventana, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
entry_usuario = ttk.Entry(ventana)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(ventana, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
entry_password = ttk.Entry(ventana, show="*")  # Oculta el texto ingresado
entry_password.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(ventana, text="Ingresar", command=validar_login).grid(row=2, column=0, columnspan=2, pady=10)

ventana.mainloop()
