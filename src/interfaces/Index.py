import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
from fpdf import FPDF

sys.path.append("src")
from model.Usuario import Usuario
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Tarea import Tarea


class ToDoApp:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Aplicación To Do")
        self.root.geometry("400x300")

        # Título
        self.label = tk.Label(root, text=f"Bienvenid@ {self.usuario.nombre}", font=("Helvetica", 14))
        self.label.pack(pady=20)

        # Botón Crear Tarea
        self.btn_create_task = tk.Button(root, text="Crear tarea", command=self.crear_tarea, width=20)
        self.btn_create_task.pack(pady=10)

        # Botón Ver/Editar Tareas
        self.btn_view_edit_tasks = tk.Button(root, text="Ver/Editar tareas", command=self.ver_editar_tareas, width=20)
        self.btn_view_edit_tasks.pack(pady=10)

        # Botón Eliminar Tarea
        self.btn_delete_task = tk.Button(root, text="Eliminar tarea", command=self.eliminar_tarea, width=20)
        self.btn_delete_task.pack(pady=10)

        # Botón Exportar Tareas a PDF
        self.btn_export_tasks = tk.Button(root, text="Exportar Tareas a PDF", command=self.exportar_tareas_pdf, width=20)
        self.btn_export_tasks.pack(pady=10)

        # Botón Crear Categoría
        self.btn_create_category = tk.Button(root, text="Crear categoría", command=self.crear_categoria, width=20)
        self.btn_create_category.pack(pady=10)

        # Botón Salir
        self.btn_exit = tk.Button(root, text="Salir", command=self.salir, width=20)
        self.btn_exit.pack(pady=10)

    def crear_tarea(self):
        titulo = simpledialog.askstring("Crear tarea", "Ingrese el título de la tarea:")
        descripcion = simpledialog.askstring("Crear tarea", "Ingrese la descripción de la tarea:")
        fecha_limite = simpledialog.askstring("Crear tarea", "Ingrese la fecha límite (YYYY-MM-DD):")
        prioridad = simpledialog.askstring("Crear tarea", "Ingrese la prioridad (Alta, Media, Baja):")

        categorias = Controlador_Usuarios.Listar_Categorias(self.usuario)
        if categorias:
            categoria_str = "\n".join([f"{idx + 1}. {cat[0]}" for idx, cat in enumerate(categorias)])
            cat_index = simpledialog.askinteger("Seleccionar categoría", f"Categorías disponibles:\n{categoria_str}\nSeleccione una categoría:")
            if cat_index and 1 <= cat_index <= len(categorias):
                categoria_id = categorias[cat_index - 1][1]
            else:
                messagebox.showerror("Error", "Categoría no válida.")
                return
        else:
            Controlador_Usuarios.Crear_Categoria_General(self.usuario)
            categoria_id = 1  # ID de la categoría general

        tarea = Tarea(titulo, descripcion, fecha_limite, prioridad)
        Controlador_Usuarios.Insertar_Tarea(tarea, self.usuario, categoria_id)
        messagebox.showinfo("Éxito", "Tarea creada exitosamente.")

    def ver_editar_tareas(self):
        tareas = Controlador_Usuarios.Listar_Tareas(self.usuario)
        if not tareas:
            messagebox.showinfo("Información", "No tienes tareas.")
            return

        tarea_info = "\n".join([f"Título: {t[0]}, Descripción: {t[1]}, Fecha Límite: {t[2]}, Prioridad: {t[3]}" for t in tareas])
        titulo = simpledialog.askstring("Ver/Editar tareas", f"Lista de Tareas:\n{tarea_info}\nIngrese el título de la tarea que desea editar (o presione Cancelar para salir):")

        if titulo:
            nueva_descripcion = simpledialog.askstring("Editar tarea", "Nueva Descripción:")
            nueva_fecha_limite = simpledialog.askstring("Editar tarea", "Nueva Fecha Límite (YYYY-MM-DD):")
            nueva_prioridad = simpledialog.askstring("Editar tarea", "Nueva Prioridad (Alta, Media, Baja):")
            nueva_tarea = Tarea(titulo, nueva_descripcion, nueva_fecha_limite, nueva_prioridad)
            Controlador_Usuarios.Actualizar_Tarea(titulo, nueva_tarea, self.usuario)
            messagebox.showinfo("Éxito", "Tarea editada exitosamente.")

    def eliminar_tarea(self):
        titulo = simpledialog.askstring("Eliminar tarea", "Ingrese el título de la tarea que desea eliminar:")
        Controlador_Usuarios.Eliminar_Tarea(titulo, self.usuario)
        messagebox.showinfo("Éxito", "Tarea eliminada exitosamente.")

    def crear_categoria(self):
        nombre_categoria = simpledialog.askstring("Crear categoría", "Ingrese el nombre de la nueva categoría:")
        Controlador_Usuarios.Crear_Categoria(nombre_categoria, self.usuario)
        messagebox.showinfo("Éxito", "Categoría creada exitosamente.")

    def exportar_tareas_pdf(self):
        tareas = Controlador_Usuarios.Listar_Tareas(self.usuario)
        if not tareas:
            messagebox.showinfo("Información", "No hay tareas para exportar.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Tareas de {self.usuario.nombre}", ln=True, align="C")
        pdf.set_font("Arial", size=12)

        for tarea in tareas:
            pdf.cell(0, 10, f"Título: {tarea[0]}", ln=True)
            pdf.cell(0, 10, f"Descripción: {tarea[1]}", ln=True)
            pdf.cell(0, 10, f"Fecha Límite: {tarea[2]}", ln=True)
            pdf.cell(0, 10, f"Prioridad: {tarea[3]}", ln=True)
            pdf.cell(0, 10, "", ln=True)  # Línea en blanco entre tareas

        pdf_file_name = f"{self.usuario.nombre}_tareas.pdf"
        pdf.output(pdf_file_name)
        messagebox.showinfo("Éxito", f"Tareas exportadas a {pdf_file_name} correctamente.")

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.destroy()


class Ejecutar_App:
    def Iniciar_App(usuario):
        root = tk.Tk()
        app = ToDoApp(root, usuario)
        root.mainloop()
