import tkinter as tk
from tkinter import messagebox
import sys

sys.path.append("src")
from interfaces.Index import Ejecutar_App
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario


class IniciarSesionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Iniciar Sesión")
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

        # Botón para iniciar sesión
        self.btn_iniciar = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_iniciar.pack(pady=20)

        # Botón para salir
        self.btn_exit = tk.Button(root, text="Salir", command=self.salir)
        self.btn_exit.pack(pady=5)

    def iniciar_sesion(self):
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()

        if not nombre or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Crear la instancia del usuario
        usuario = Usuario(nombre, contrasena)

        # Intentar iniciar sesión
        try:
            resultado = Controlador_Usuarios.Iniciar_Sesión(usuario)
            if resultado:
                raise Exception("ERROR: Usuario o contraseña incorrectos")
            
            # Si la sesión se inicia correctamente, abrir la página principal
            Ejecutar_App.Iniciar_App(usuario)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.destroy()

class Ejecutar_Inicio_Sesion:
    def Iniciar_Sesion():
        root = tk.Tk()
        app = IniciarSesionApp(root)
        root.mainloop()
