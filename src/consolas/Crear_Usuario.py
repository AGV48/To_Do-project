from os import system
# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

class Crear_Usuario:
    def Registrar_Usuario():
        print("---------------------------------------------------------------------")
        print("                     To Do                 ")
        print("DATOS PERSONALES")
        # Se obtienen los datos de entrada
        nombre = str(input("Por favor ingrese su nombre de usuario: "))
        contrasena = str(input("Por favor ingrese su contraseña: "))
        print("-------------------------------------------------------------------------")
        system("cls")

        #Se crea el usuario en la base de datos
        usuario = Usuario(nombre, contrasena)
        Controlador_Usuarios.Insertar_Usuario(usuario)
        return