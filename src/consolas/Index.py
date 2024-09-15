# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

class Aplicacion:
    def Pagina_Principal(usuario):
        print("---------------------------------------------------------------------")
        print("                     To Do                 ")
        print(f"Bienvenid@ {usuario}, próximamente tendremos las funcionalidades disponibles, te invitamos a estar atent@")
        print("-------------------------------------------------------------------------")

        # Como aún no hay ninguna funcionalidad, se termina la ejecución del software
        sys.exit()
        