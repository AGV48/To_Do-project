# Lo importamos para ir limpiando la consola mientras el software se ejecuta
from os import system

# Lo importamos para poder incluir la ruta de búsqueda python
import sys
sys.path.append("src")

# Lo importamos para poder realizar las consultas en la base de datos
import psycopg2

# Se importa el modulo donde se realizarán los procesos
from controladores import Secret_Config
from model.Usuario import Usuario
from model.Tarea import Tarea

class Controlador_Usuarios:

    # Todas las consultas se realizan mediante un cursor, por lo que se crea un método para obtenerlo
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
    
    # Método para crear la tabla usuarios en la base de datos
    def Crear_Tabla_Usuarios():
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
    
    # Agrega esto en la clase Controlador_Usuarios

    # Agrega esto en la clase Controlador_Usuarios

    # Método para crear la tipo de prioridades en la base de datos
    def Crear_Prioridades():
        """ 
        Crea la tabla de prioridades en la base de datos 
        """
        try:
            # Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            cursor.execute("""create type prioridades as enum('Alta', 'Media', 'Baja')""")

            cursor.connection.commit()
        except Exception as e:
            # Si ocurre algún error, revierte la transacción y devuelve un mensaje
            cursor.connection.rollback()
            return f"Error al crear la tabla de prioridades: {e}"

        return "Tipo Creado"

    # Método para crear la tabla de tareas en la base de datos
    def Crear_Tabla_Tareas():
        """ 
        Crea la tabla de tareas en la base de datos 
        """

        try:
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            #Se ejecuta el query para crear la tabla en la base de datos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    titulo VARCHAR(100) NOT NULL,
                    descripcion VARCHAR(200) NOT NULL,
                    fecha_limite DATE NOT NULL,
                    prioridad prioridades NOT NULL,
                    usuario VARCHAR(50) REFERENCES usuarios(usuario) ON DELETE CASCADE,
                    categoria_id INT REFERENCES categorias(id),
                    PRIMARY KEY (titulo, usuario)
                )
            """)

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()

        # En caso de que ocurra un error, se imprime el error
        except Exception as e:
            cursor.connection.rollback()
            return f"Error al crear la tabla de tareas: {e}"
        return "Tabla Creada"

    def Crear_Tabla_Categorias():
        """
        Crea la tabla de categorías en la base de datos
        """

        try:
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            #Se ejecuta el query para crear la tabla en la base de datos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    usuario VARCHAR(50) REFERENCES usuarios(usuario) ON DELETE CASCADE
                )
            """)

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()

        # En caso de que ocurra un error, se imprime el error
        except Exception as e:
            cursor.connection.rollback()
            return f"Error al crear la tabla de categorias: {e}"
        return "Tabla Creada"

    def Crear_Categoria_General(usuario):
        """
        Crea la categoría 'General' para el usuario
        """

        # Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        try:
            # Se inserta la categoría en la base de datos
            cursor.execute(
                f"INSERT INTO categorias (nombre, usuario) VALUES ('General', '{usuario}')"
            )

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()

        # En caso de error, se imprime el error
        except Exception as e:
            cursor.connection.rollback()

    # Método para insertar un usuario en la base de datos
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
    
    # Método para insertar una tarea en la base de datos
    def Insertar_Tarea(tarea, usuario, categoria_id=None):
        """ 
        Inserta una tarea en la tabla tareas asociada a un usuario.
        Si no existe una categoría, crea la categoría 'General' y la usa por defecto.
        """
        # Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        # Verificar si la categoría 'General' ya existe para el usuario
        cursor.execute(f"""
            SELECT id FROM categorias 
            WHERE nombre = 'General' AND usuario = '{usuario}'
        """)
        categoria_general = cursor.fetchone()

        # Si la categoría 'General' no existe, se crea y obtiene su ID
        if not categoria_general:
            cursor.execute(f"""
                INSERT INTO categorias (nombre, usuario) 
                VALUES ('General', '{usuario}')
                RETURNING id
            """)
            categoria_general = cursor.fetchone()
            cursor.connection.commit()  # Asegura el cambio en la base de datos

        # Usa la categoría 'General' si no se especificó otra
        categoria_id = categoria_id or categoria_general[0]

        try:
            # Inserta la tarea con la categoría especificada o 'General'
            cursor.execute(
                f"""INSERT INTO tareas (titulo, descripcion, fecha_limite, prioridad, usuario, categoria_id) 
                    VALUES ('{tarea.titulo}', '{tarea.descripcion}', '{tarea.fecha_limite}', '{tarea.prioridad}', '{usuario}', {categoria_id})"""
            )

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()
            print("Tarea creada exitosamente")

        except Exception as e:
            cursor.connection.rollback()
            print(f"Error al crear la tarea: {e}")

    # Método para listar todas las tareas
    def Listar_Tareas(usuario: Usuario):
        """ 
        Devuelve todas las tareas creadas por un usuario específico 
        """

        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        # Se ejecuta el query para traer todas las tareas de un usuario
        cursor.execute(f"SELECT titulo, descripcion, fecha_limite, prioridad FROM tareas WHERE usuario = '{usuario.nombre}'")

        # Se guardan todas las tareas en una variable
        tareas = cursor.fetchall()

        # Se retorna la lista de tareas
        return tareas

    # Método para actualizar una tarea en la base de datos
    def Actualizar_Tarea(titulo, nueva_tarea: Tarea, usuario: Usuario):
        """ 
        Actualiza la información de una tarea en la base de datos si pertenece al usuario especificado 
        """

        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        # Se verifica que la tarea pertenezca al usuario antes de actualizar
        cursor.execute(f"""
            UPDATE tareas 
            SET descripcion = '{nueva_tarea.descripcion}', 
                fecha_limite = '{nueva_tarea.fecha_limite}', 
                prioridad = '{nueva_tarea.prioridad}' 
            WHERE titulo = '{titulo}' AND usuario = '{usuario.nombre}'
        """)

        # Confirma los cambios realizados en la base de datos
        cursor.connection.commit()

        # Se limpia la consola para que todo se vea organizado
        system("cls")
        print("TAREA ACTUALIZADA CORRECTAMENTE")

    # Método para eliminar una tarea de la base de datos
    def Eliminar_Tarea(titulo, usuario: Usuario):
        """ 
        Elimina una tarea de la base de datos usando su título si pertenece al usuario especificado 
        """

        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        try:
            # Elimina la tarea solo si pertenece al usuario indicado
            cursor.execute(f"DELETE FROM tareas WHERE titulo = '{titulo}' AND usuario = '{usuario.nombre}'")

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()
            print(f"TAREA '{titulo}' ELIMINADA CORRECTAMENTE")

        except Exception as e:
            # En caso de error, revierte la transacción
            cursor.connection.rollback()
            print(f"Error al eliminar la tarea: {e}")

    def Crear_Categoria(nombre_categoria, usuario):
        """
        Crea una nueva categoría para el usuario
        """

        # Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        try:
            # Se inserta la categoría en la base de datos
            cursor.execute(
                f"INSERT INTO categorias (nombre, usuario) VALUES ('{nombre_categoria}', '{usuario}')"
            )

            # Confirma los cambios realizados en la base de datos
            cursor.connection.commit()
            print("Categoría creada exitosamente")

        # En caso de error, se imprime el error
        except Exception as e:
            cursor.connection.rollback()
            print(f"Error al crear la categoría: {e}")

    def Listar_Categorias(usuario):
        """
        Lista las categorías de un usuario
        """

        # Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        # Se ejecuta el query para traer todas las categorías de un usuario
        cursor.execute(f"SELECT nombre, id FROM categorias WHERE usuario = '{usuario}'")

        # Se retornan todas las categorías
        return cursor.fetchall()

    # Método para buscar usuarios en la base de datos y ver si existen
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

    # Método para actualizar la contraseña de un usuario
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

    # Método para iniciar sesión en el software
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
            # Si estos datos son incorrectos, retoma un TRUE
            return True
        else:
            # Si estos datos son correctos, retorna un FALSE
            return False

    # Verifica que ningún campo haya quedado vacío
    def verificarValores_vacios(nombre, contrasena):
        if nombre == "" or contrasena == "":
            raise Exception("ERROR: No pueden haber campos vacíos")
    
    # Verifica que la contraseña cumpla con la cantidad minima de caracteres
    def verificarContrasena(contrasena):
        if len(contrasena) < 8:
            raise Exception("ERROR: La contraseña debe tener mínimo 8 caracteres")
        
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
        
    # Verifica que ningún campo de una tarea haya quedado vacío o inválido
    def verificarValores_Tarea(titulo, descripcion, fecha_limite, prioridad):
        if titulo == "":
            raise Exception("ERROR: El título de la tarea no puede estar vacío")
        
        if descripcion == "":
            raise Exception("ERROR: La descripción de la tarea no puede estar vacía")
        
        if fecha_limite == "":
            raise Exception("ERROR: La fecha límite de la tarea no puede estar vacía")
        
        # Validar que la prioridad esté dentro de los valores permitidos
        prioridades_validas = ["Alta", "Media", "Baja"]
        if prioridad not in prioridades_validas:
            raise Exception(f"ERROR: La prioridad debe ser una de las siguientes: {', '.join(prioridades_validas)}")
