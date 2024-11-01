import tkinter as tk
from tkinter import messagebox
import sys

sys.path.append("src")
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario


class CambiarContrasenaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambiar Contraseña")
        self.root.geometry("300x200")

        # Etiquetas y campos de entrada
        self.label_nombre = tk.Label(root, text="Nombre de usuario:")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack(pady=5)

        self.label_contrasena = tk.Label(root, text="Nueva Contraseña:")
        self.label_contrasena.pack(pady=5)

        self.entry_contrasena = tk.Entry(root, show='*')
        self.entry_contrasena.pack(pady=5)

        # Botón para cambiar la contraseña
        self.btn_cambiar = tk.Button(root, text="Cambiar Contraseña", command=self.cambiar_contrasena)
        self.btn_cambiar.pack(pady=20)

        # Botón para salir
        self.btn_exit = tk.Button(root, text="Salir", command=self.salir)
        self.btn_exit.pack(pady=5)

    def cambiar_contrasena(self):
        nombre = self.entry_nombre.get()
        nueva_contrasena = self.entry_contrasena.get()

        if not nombre or not nueva_contrasena:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Crear la instancia del usuario
        usuario = Usuario(nombre, nueva_contrasena)

        # Intentar cambiar la contraseña
        try:
            Controlador_Usuarios.Actualizar_Usuario(nombre, usuario)
            messagebox.showinfo("Éxito", "La contraseña se ha cambiado correctamente.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_contrasena.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.destroy()

class Ejecutar_Cambiar_Contrasena:
    def Asignar_Nueva_Contrasena():
        root = tk.Tk()
        app = CambiarContrasenaApp(root)
        root.mainloop()
