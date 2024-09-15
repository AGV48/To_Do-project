# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from consolas.Index import Aplicacion
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

class Iniciar_Sesion:
    # Metodo donde se realizará todo el proceso de inicio de sesión
    def Ingresar_Al_Software():
        print("---------------------------------------------------------------------")
        print("                     To Do                 ")
        print("INGRESO A LA PLATAFORMA")
        # Se obtienen los datos de entrada
        nombre = str(input("Por favor ingrese su nombre de usuario: "))
        contrasena = str(input("Por favor ingrese su contraseña: "))
        print("-------------------------------------------------------------------------")
        # Se limpia la consola para que todo se vea organizado
        system("cls")

        # Se crea la instancia del usuario
        usuario = Usuario(nombre, contrasena)

        # Se busca el usuario con su respectiva contraseña en la base de datos
        resultado = Controlador_Usuarios.Iniciar_Sesión(usuario)
        
        # Si la contraseña es incorrecta, el usuario es incorrecto o el usuario no existe en la base de datos, se lanza un error
        if resultado:
            raise Exception("ERROR: Usuario o contraseña incorrectos")
        
        # Si el usuario y la contraseña son correctos, se lleva a la pagina principal del software
        Aplicacion.Pagina_Principal(usuario)