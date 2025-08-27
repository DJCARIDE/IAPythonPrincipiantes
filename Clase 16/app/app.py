# app.py
# Archivo principal de la aplicación Tkinter.
# Contiene la interfaz de usuario y la lógica de eventos.

import tkinter as tk
from tkinter import ttk, messagebox

# Importar componentes desde los otros archivos
from config import DB_CONFIG
from database import DatabaseManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Clientes con MySQL")
        self.root.geometry("900x650")

        # Crear instancia del gestor de base de datos
        self.db_manager = DatabaseManager(DB_CONFIG)

        # Crear los widgets de la interfaz
        self.crear_widgets()
        
        # Cargar datos iniciales si la conexión fue exitosa
        if self.db_manager.connection:
            self.cargar_datos()
        
        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def crear_widgets(self):
        # --- Frame para la tabla ---
        frame_tabla = ttk.Frame(self.root, padding="10")
        frame_tabla.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tabla = ttk.Treeview(frame_tabla, yscrollcommand=scrollbar.set)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabla.yview)

        self.tabla['columns'] = ('ID', 'Nombre', 'Email', 'Teléfono')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.column('ID', anchor=tk.CENTER, width=50)
        self.tabla.column('Nombre', anchor=tk.W, width=200)
        self.tabla.column('Email', anchor=tk.W, width=200)
        self.tabla.column('Teléfono', anchor=tk.W, width=120)

        self.tabla.heading('#0', text='')
        self.tabla.heading('ID', text='ID', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        self.tabla.heading('Email', text='Email', anchor=tk.CENTER)
        self.tabla.heading('Teléfono', text='Teléfono', anchor=tk.CENTER)
        
        self.tabla.bind('<<TreeviewSelect>>', self.seleccionar_cliente)
        
        # --- Frame para los campos de entrada ---
        frame_inputs = ttk.LabelFrame(self.root, text="Datos del Cliente", padding="10")
        frame_inputs.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ttk.Entry(frame_inputs, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_inputs, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = ttk.Entry(frame_inputs, width=40)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_inputs, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = ttk.Entry(frame_inputs, width=40)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        frame_inputs.grid_columnconfigure(1, weight=1)

        # --- Frame para los botones ---
        frame_botones = ttk.Frame(self.root, padding="10")
        frame_botones.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        btn_agregar = ttk.Button(frame_botones, text="Agregar", command=self.agregar_cliente)
        btn_agregar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_cliente)
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_cliente)
        btn_eliminar.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        btn_limpiar = ttk.Button(frame_botones, text="Limpiar Campos", command=self.limpiar_campos)
        btn_limpiar.grid(row=3, column=0, padx=5, pady=15, sticky="ew")

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        clientes = self.db_manager.fetch_all_clientes()
        for cliente in clientes:
            self.tabla.insert('', tk.END, values=cliente)

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        
        if not nombre:
            messagebox.showwarning("Campo Vacío", "El nombre es obligatorio.")
            return
            
        if self.db_manager.insert_cliente(nombre, email, telefono):
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            self.limpiar_campos()
            self.cargar_datos()

    def actualizar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, selecciona un cliente para actualizar.")
            return
            
        client_id = self.tabla.item(seleccion[0])['values'][0]
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        
        if not nombre:
            messagebox.showwarning("Campo Vacío", "El nombre es obligatorio.")
            return

        if self.db_manager.update_cliente(client_id, nombre, email, telefono):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.limpiar_campos()
            self.cargar_datos()

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, selecciona un cliente para eliminar.")
            return
            
        cliente_info = self.tabla.item(seleccion[0])['values']
        client_id, nombre_cliente = cliente_info[0], cliente_info[1]
        
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar a {nombre_cliente}?")
        
        if respuesta:
            if self.db_manager.delete_cliente(client_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.limpiar_campos()
                self.cargar_datos()

    def seleccionar_cliente(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion: return
            
        valores = self.tabla.item(seleccion[0])['values']
        
        self.limpiar_campos(deseleccionar=False)
        self.entry_nombre.insert(0, valores[1])
        self.entry_email.insert(0, valores[2])
        self.entry_telefono.insert(0, valores[3])

    def limpiar_campos(self, deseleccionar=True):
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        
        if deseleccionar and self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])

    def on_closing(self):
        self.db_manager.close()
        self.root.destroy()


if __name__ == "__main__":
    # Crear la ventana principal
    ventana_principal = tk.Tk()
    # Iniciar la aplicación
    app = App(ventana_principal)
    # Iniciar el loop principal
    ventana_principal.mainloop()