# Definimos la clase Tarea para almacenar la información de cada tarea
class Tarea:
    def __init__(self, titulo, descripcion, fecha_limite, prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.prioridad = prioridad

    def __str__(self):
        return f"Tarea: {self.titulo}\nDescripción: {self.descripcion}\nFecha límite: {self.fecha_limite}\nPrioridad: {self.prioridad}\n"
