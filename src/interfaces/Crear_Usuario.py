import tkinter as tk
from tkinter import messagebox
import sys

sys.path.append("src")
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario


class CrearUsuarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Usuario")
        self.root.geometry("300x200")

        # Etiquetas y campos de entrada
        self.label_nombre = tk.Label(root, text="Nombre de usuario:")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack(pady=5)

        self.label_contrasena = tk.Label(root, text="Contraseña:")
        self.label_contrasena.pack(pady=5)

        self.entry_contrasena = tk.Entry(root, show='*')
        self.entry_contrasena.pack(pady=5)

        # Botón para registrar
        self.btn_registrar = tk.Button(root, text="Registrar", command=self.registrar_usuario)
        self.btn_registrar.pack(pady=20)

        # Botón para salir
        self.btn_exit = tk.Button(root, text="Salir", command=self.salir)
        self.btn_exit.pack(pady=5)

    def registrar_usuario(self):
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()

        if not nombre or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Crear la instancia del usuario
        usuario = Usuario(nombre, contrasena)

        # Intentar insertar el usuario en la base de datos
        try:
            Controlador_Usuarios.Insertar_Usuario(usuario)
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_contrasena.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.destroy()

class Ejecutar_Registro:
    def Registrar_Usuario():
        root = tk.Tk()
        app = CrearUsuarioApp(root)
        root.mainloop()
