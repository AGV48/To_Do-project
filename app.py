# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from consolas.Crear_Usuario import Crear_Usuario
from consolas.Cambiar_Contrasena import Cambiar_Contrasena
from consolas.Iniciar_Sesion import Iniciar_Sesion
from controladores.Controlador_Usuarios import Controlador_Usuarios
from model.Usuario import Usuario

# Se le da una bienvenida al usuario y se le muestra un menú con las opciones
def Bienvenida():
    print("-------------------------------------------")
    print("    BIENVENID@ A TU APLICACIÓN DE To Do   ")
    print("¿Qué deseas hacer?")
    print(" 1.Iniciar Sesión, 2.Registrarse, 3.Cambiar Contraseña, 0.Salir")
    opcion = int(input("Elija una opción: "))
    print("--------------------------------------")
    # Se llama a la siguiente función y se le pasa como parametro la opción que el usuario eligió
    return desiciones(opcion)

def desiciones(opcion):
    # Se hace uso del metodo try para lanzar una excepción si algo falla
    try:
        # Se usa el ciclo while para verificar cual opción escogio el usuario
        while opcion != 0:
            # Se verifica si la opción escogida por el usuario no está definida
            if opcion < 1 or opcion > 3:
                system("cls")
                print("------------------------------------------------------------------")
                print("                  To Do            ")
                print("La opción ingresada no es correcta, intente de nuevo")
                print("-------------------------------------------------------------------")
                # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
                Bienvenida()
            
            # Se verifica si el usuario quiere iniciar sesión en el software
            if opcion == 1:
                # Se limpia la consola para que todo se vea organizado
                system("cls")

                # Se llama la función "Ingresar_Al_Software" para llevar al usuario hasta allí
                Iniciar_Sesion.Ingresar_Al_Software()

            # Se verifica si el usuario quiere crear una cuenta en el software
            if opcion == 2:
                # Se limpia la consola para que todo se vea organizado
                system("cls")
                
                # Se llama la función "Registrar_Usuario" para llevar al usuario hasta allí
                Crear_Usuario.Registrar_Usuario()
                # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
                Bienvenida()

            # Se verifica si el usuario quiere cambiar la contraseña de su cuenta
            if opcion == 3:
                # Se limpia la consola para que todo se vea organizado
                system("cls")
                
                # Se llama la función "Asignar_Nueva_Contrasena" para llevar al usuario hasta allí
                Cambiar_Contrasena.Asignar_Nueva_Contrasena()
                # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
                Bienvenida()

        # Se le da al usuario un mensaje de despedida al usuario cuando finaliza todo el proceso
        print("------------------------------------------------------------------")
        print("                  To Do            ")
        print("Gracias por visitarnos, vuelva pronto")
        print("-------------------------------------------------------------------")
        # Se termina el programa
        sys.exit()
    # Se lanza un mensaje de error cuando algo falla
    except Exception as exc:
        print("------------------------------------------------------------------")
        print("                  To Do            ")
        print(f"{exc}, intentalo nuevamente")
        print("-------------------------------------------------------------------")
        # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
        Bienvenida()

#Condicional para comprobar si la tabla "Usuarios" ya está creada
if Controlador_Usuarios.Crear_Tabla() == "Tabla Existente":
    # Si la condición anterior se cumple, solo se llama la funcion para dar inicio al programa
    Bienvenida()

else:
    #Si la condición anterior no se cumple, se crea la tabla en la base de datos
    Controlador_Usuarios.Crear_Tabla()
    # Se llama la funcion para dar inicio al programa
    Bienvenida()
