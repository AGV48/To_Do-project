from os import system
# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from consolas.Index import Aplicacion
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

class Iniciar_Sesion:
    def Ingresar_Al_Software():
        print("---------------------------------------------------------------------")
        print("                     To Do                 ")
        print("INGRESO A LA PLATAFORMA")
        # Se obtienen los datos de entrada
        nombre = str(input("Por favor ingrese su nombre de usuario: "))
        contrasena = str(input("Por favor ingrese su contraseña: "))
        print("-------------------------------------------------------------------------")
        system("cls")

        #Se crea el usuario en la base de datos
        usuario = Usuario(nombre, contrasena)
        resultado = Controlador_Usuarios.Iniciar_Sesión(usuario)
        
        if resultado:
            raise Exception("ERROR: Usuario o contraseña incorrectos")
        
        Aplicacion.Pagina_Principal(usuario)