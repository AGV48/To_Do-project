from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")


import psycopg2

from controladores import Secret_Config
from model.Usuario import Usuario


class Controlador_Usuarios:

    def Obtener_Cursor():
        """
        Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
        """
        DATABASE = Secret_Config.PGDATABASE
        USER = Secret_Config.PGUSER
        PASSWORD = Secret_Config.PGPASSWORD
        HOST = Secret_Config.PGHOST
        PORT = Secret_Config.PGPORT
        #Se realiza la conexión con la base de datos
        connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor = connection.cursor()
        return cursor
    
    def Crear_Tabla():
        """ 
        Crea la tabla de usuarios en la BD 
        """
        try:
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            #Se ejecuta el query para crear la tabla en la base de datos
            cursor.execute("""create table usuarios (usuario varchar(50) not null primary key, 
                            contrasena varchar(30) not null)""")
            
            # Confirma los cambios realizados en la base de datos
            # Si no se llama, los cambios no quedan aplicados
            cursor.connection.commit()
        except:
            #Si llega aquí es porque la tabla ya existe y no se pudo crear
            cursor.connection.rollback()
            return "Tabla Existente"
        
    def Insertar_Usuario( usuario : Usuario ):
            """ 
            Recibe una instancia de la clase Usuario y la inserta en la tabla respectiva
            """
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            Controlador_Usuarios.verificarValores_vacios(usuario.nombre, usuario.contrasena)
            Controlador_Usuarios.verificarContrasena(str(usuario.contrasena))
            Controlador_Usuarios.verificarExistenciaUsuario_Insercion(usuario.nombre)
            

            cursor.execute(f"""insert into usuarios (usuario, contrasena) values ('{usuario.nombre}', '{usuario.contrasena}')""")
            cursor.connection.commit()
            system("cls")
            print("USUARIO CREADO CORRECTAMENTE")
            print("\n")
    
    def Buscar_Usuario( usuario_buscado ):
        """ 
        Trae un usuario de la tabla de usuarios por el nombre
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        #Se ejecuta el query para buscar el usuario por su cédula
        cursor.execute(f"""select usuario from usuarios where usuario = '{usuario_buscado}'""" )
        if cursor.fetchone() ==  None:
            return False
        else:
            return True

    def Actualizar_Usuario( usuario_buscado, datos_actualizar: Usuario ):
        """ 
        Trae un usuario de la tabla de usuarios por la cedula y actualiza sus valores
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        Controlador_Usuarios.verificarValores_vacios(datos_actualizar.nombre, datos_actualizar.contrasena)
        Controlador_Usuarios.verificarContrasena(datos_actualizar.contrasena)
        Controlador_Usuarios.verificarExistenciaUsuario_Actualizacion(usuario_buscado)
        
        cursor.execute(f"""update usuarios set contrasena = '{datos_actualizar.contrasena}' where usuario = '{usuario_buscado}'""")
        cursor.connection.commit()
        system("cls")
        print("CONTRASEÑA ACTUALIZADA CORRECTAMENTE")

    def Iniciar_Sesión(usuario):
        """ 
        Buscar un usuario de la tabla de usuarios por el nombre
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        Controlador_Usuarios.verificarValores_vacios(usuario.nombre, usuario.contrasena)

        #Se ejecuta el query para buscar el usuario por su cédula
        cursor.execute(f"""select usuario, contrasena from usuarios where usuario = '{usuario.nombre}' and contrasena = '{usuario.contrasena}'""" )
        if cursor.fetchone() ==  None:
            return True
        else:
            return False

    # Verifica que ningun campo haya quedado vacio
    def verificarValores_vacios(nombre, contrasena):
        if nombre == "" or contrasena == "":
            raise Exception("ERROR: No pueden haber campos vacios")
    
    def verificarContrasena(contrasena):
        if len(contrasena) < 8:
            raise Exception("ERROR: La contraseña debe tener minimo 8 caracteres")
        
    def verificarExistenciaUsuario_Insercion(nombre):
        usuario_existe = Controlador_Usuarios.Buscar_Usuario(nombre)
        if usuario_existe:
            raise Exception("ERROR: Ya existe un usuario con ese nombre")
        
    def verificarExistenciaUsuario_Actualizacion(nombre):
        usuario_existe = Controlador_Usuarios.Buscar_Usuario(nombre)
        if not usuario_existe:
            raise Exception("ERROR: El usuario buscado no existe")