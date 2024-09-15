# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Lo importamos para poder realizar las consultas en la base de datos
import psycopg2

# Se importa el modulo donde se realizarán los procesos
from controladores import Secret_Config
from model.Usuario import Usuario


class Controlador_Usuarios:

    # Todas las consultas se realizan mediante un cursor, por lo que se crea un metodo para obtenerlo
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

        # Se crea la variable donde se guardará el cursor que ejecutara las consultas
        cursor = connection.cursor()
        return cursor
    
    # Metodo para crear la tabla usuarios en la base de datos
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
    
    # Metodo para insertar un usuario en la base de datos
    def Insertar_Usuario( usuario : Usuario ):
            """ 
            Recibe una instancia de la clase Usuario y la inserta en la tabla respectiva
            """
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            # Se realizan las verificaciones de que todos los campos ingresados sean correctos
            Controlador_Usuarios.verificarValores_vacios(usuario.nombre, usuario.contrasena)
            Controlador_Usuarios.verificarContrasena(str(usuario.contrasena))
            Controlador_Usuarios.verificarExistenciaUsuario_Insercion(usuario.nombre)
            
            # Si todas las verificaciones fueron exitosas, se inserta en usuario en la base de datos
            cursor.execute(f"""insert into usuarios (usuario, contrasena) values ('{usuario.nombre}', '{usuario.contrasena}')""")

            # Confirma los cambios realizados en la base de datos
            # Si no se llama, los cambios no quedan aplicados
            cursor.connection.commit()

            # Se limpia la consola para que todo se vea organizado
            system("cls")
            print("USUARIO CREADO CORRECTAMENTE")
            print("\n")
    
    # Metodo para buscar usuarios en la base de datos y ver si existen
    def Buscar_Usuario( usuario_buscado ):
        """ 
        Trae un usuario de la tabla de usuarios por el nombre
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        #Se ejecuta el query para buscar el usuario por su cédula
        cursor.execute(f"""select usuario from usuarios where usuario = '{usuario_buscado}'""" )

        # Condicionar para validar si el usuario se encontró en la base de datos
        if cursor.fetchone() ==  None:
            # Si el usuario no existe, retorna FALSE
            return False
        else:
            # Si el usuario si existe, retorna TRUE
            return True

    # Metodo para actualizar la contraseña de un usuario
    def Actualizar_Usuario( usuario_buscado, datos_actualizar: Usuario ):
        """ 
        Trae un usuario de la tabla de usuarios por la cedula y actualiza sus valores
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()
        
        # Se realizan las verificaciones de que todos los campos ingresados sean correctos
        Controlador_Usuarios.verificarValores_vacios(datos_actualizar.nombre, datos_actualizar.contrasena)
        Controlador_Usuarios.verificarContrasena(datos_actualizar.contrasena)
        Controlador_Usuarios.verificarExistenciaUsuario_Actualizacion(usuario_buscado)
        
        # Si todas las verificaciones fueron exitosas, se inserta en usuario en la base de datos
        cursor.execute(f"""update usuarios set contrasena = '{datos_actualizar.contrasena}' where usuario = '{usuario_buscado}'""")

        # Confirma los cambios realizados en la base de datos
        # Si no se llama, los cambios no quedan aplicados
        cursor.connection.commit()

        # Se limpia la consola para que todo se vea organizado
        system("cls")
        print("CONTRASEÑA ACTUALIZADA CORRECTAMENTE")

    # Metodo para iniciar sesión en el software
    def Iniciar_Sesión(usuario):
        """ 
        Recibe un usuario (nombre, contraseña) como parametro y busca que estén en la base de datos
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        # Se realizan las verificaciones de que todos los campos ingresados sean correctos
        Controlador_Usuarios.verificarValores_vacios(usuario.nombre, usuario.contrasena)

        #Se ejecuta el query para buscar el usuario y la contraseña en la base de datos
        cursor.execute(f"""select usuario, contrasena from usuarios where usuario = '{usuario.nombre}' and contrasena = '{usuario.contrasena}'""" )

        # Condicionar para validar si el usuario y la contraseña son correctos y están en la base de datos
        if cursor.fetchone() ==  None:
            # Si estos datos son incorrectos, retorma un TRUE
            return True
        else:
            # Si estos datos son correctos, retorma un FALSE
            return False

    # Verifica que ningun campo haya quedado vacio
    def verificarValores_vacios(nombre, contrasena):
        if nombre == "" or contrasena == "":
            raise Exception("ERROR: No pueden haber campos vacios")
    
    # Verifica que la contraseña cumpla con la cantidad minima de caracteres
    def verificarContrasena(contrasena):
        if len(contrasena) < 8:
            raise Exception("ERROR: La contraseña debe tener minimo 8 caracteres")
        
    # Verifica que el usuario no exista en la base de datos para poder insertarlo
    def verificarExistenciaUsuario_Insercion(nombre):
        usuario_existe = Controlador_Usuarios.Buscar_Usuario(nombre)
        if usuario_existe:
            raise Exception("ERROR: Ya existe un usuario con ese nombre")
        
    # Verifica que el usuario exista en la base de datos para poder cambiar su contraseña
    def verificarExistenciaUsuario_Actualizacion(nombre):
        usuario_existe = Controlador_Usuarios.Buscar_Usuario(nombre)
        if not usuario_existe:
            raise Exception("ERROR: El usuario buscado no existe")