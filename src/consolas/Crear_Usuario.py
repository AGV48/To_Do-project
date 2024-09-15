# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

class Crear_Usuario:
    # Metodo donde se realizará todo el proceso de registro
    def Registrar_Usuario():
        print("---------------------------------------------------------------------")
        print("                     To Do                 ")
        print("DATOS PERSONALES")
        # Se obtienen los datos de entrada
        nombre = str(input("Por favor ingrese su nombre de usuario: "))
        contrasena = str(input("Por favor ingrese su contraseña: "))
        print("-------------------------------------------------------------------------")
        # Se limpia la consola para que todo se vea organizado
        system("cls")

        #Se crea la instancia del usuario
        usuario = Usuario(nombre, contrasena)

        #Se crea el usuario en la base de datos
        Controlador_Usuarios.Insertar_Usuario(usuario)
        # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
        return