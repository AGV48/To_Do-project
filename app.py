import tkinter as tk
from tkinter import messagebox
from os import system
import sys

sys.path.append("src")
from interfaces.Crear_Usuario import Ejecutar_Registro
from interfaces.Cambiar_Contrasena import Ejecutar_Cambiar_Contrasena
from interfaces.Iniciar_Sesion import Ejecutar_Inicio_Sesion
from controladores.Controlador_Usuarios import Controlador_Usuarios


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación To Do")
        self.root.geometry("400x300")

        # Título
        self.label = tk.Label(root, text="Bienvenid@ a tu Aplicación de To Do", font=("Helvetica", 14))
        self.label.pack(pady=20)

        # Botón Iniciar Sesión
        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion, width=20)
        self.btn_login.pack(pady=10)

        # Botón Registrarse
        self.btn_register = tk.Button(root, text="Registrarse", command=self.registrar_usuario, width=20)
        self.btn_register.pack(pady=10)

        # Botón Cambiar Contraseña
        self.btn_change_password = tk.Button(root, text="Cambiar Contraseña", command=self.cambiar_contrasena, width=20)
        self.btn_change_password.pack(pady=10)

        # Botón Salir
        self.btn_exit = tk.Button(root, text="Salir", command=self.salir, width=20)
        self.btn_exit.pack(pady=10)

        # Verificación de tablas
        self.verificar_tablas()

    def verificar_tablas(self):
        if (Controlador_Usuarios.Crear_Tabla_Usuarios() == "Tabla Existente" and
                Controlador_Usuarios.Crear_Tabla_Tareas() == "Tabla Existente" and
                Controlador_Usuarios.Crear_Tabla_Categorias() == "Tabla Existente"):
            return
        else:
            if (Controlador_Usuarios.Crear_Prioridades() != "Tipo Creado"):
                Controlador_Usuarios.Crear_Prioridades()
            Controlador_Usuarios.Crear_Tabla_Usuarios()
            Controlador_Usuarios.Crear_Tabla_Tareas()
            Controlador_Usuarios.Crear_Tabla_Categorias()

    def iniciar_sesion(self):
        try:
            Ejecutar_Inicio_Sesion.Iniciar_Sesion()
        except Exception as exc:
            messagebox.showerror("Error", f"{exc}, inténtalo nuevamente")

    def registrar_usuario(self):
        try:
            Ejecutar_Registro.Registrar_Usuario()
        except Exception as exc:
            messagebox.showerror("Error", f"{exc}, inténtalo nuevamente")

    def cambiar_contrasena(self):
        try:
            Ejecutar_Cambiar_Contrasena.Asignar_Nueva_Contrasena()
        except Exception as exc:
            messagebox.showerror("Error", f"{exc}, inténtalo nuevamente")

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
