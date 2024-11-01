# Proyecto To Do en Python

## ¿Quién hizo esto?

- Alejandro Gutierrez Vallejo
- Tomas Ramírez Agudelo

## ¿Qué es y para qué es?

Este proyecto tiene como objetivo implementar un software para crear y administrar tareas pendientes. Funciona con una base de datos PostgreSQL para la gestión de usuarios y permite a los usuarios realizar las siguientes acciones:

- Crear, editar y eliminar tareas.
- Crear y gestionar categorías de tareas.
- Cambiar contraseñas de usuario.
- Exportar las tareas creadas a un archivo PDF.

## ¿Cómo lo hago funcionar?

1. Prerrequisitos:
### Tener una base de datos PostgreSQL:

Para esto es necesario entrar en el navegador a Neon.tech y crear una cuenta o iniciar sesión dependiendo del caso.
Estando adentro se deben seguir los siguientes pasos:

- En la pantalla darle click al botón de `Create Project` y crear un proyecto en donde se guardará la base de datos.

- Una vez se tenga el proyecto creado, Buscar en la pantalla el recuadro que dice `Connection Details`.

- Cuando se ubique el recuadro, buscar dentro de esté el apartado de "Database" y desplegar la lista y seleccionar la opción de `Create new Database` para crear la base de datos que vamos a utilizar en el proyecto. 

2. Descargar el proyecto:
Descargar los archivos de este GitHub para comenzar a trabajar en el proyecto.

3. Conectar la base de datos PostgreSQL
- Luego, en el mismo recuadro justo debajo del apartado de `Database` seleccionar el otro apartado de `Connection string`, dale click para desplegar esa lista y seleccionar la opción de `Parameters Only`, lo que aparece debajo son las credenciales que se deben poner en Python para conectarse con la base de datos (da click en `show password` para que se pueda visualizar el PGPASSWORD).

- Para realizar la conexión, las credenciales que aparecen en PostgreSQL se deben pegar en el proyecto, específicamente en el archivo `Secret_Config-sample.py` que se encuentra en la carpeta `controladores`.

### Configuración de SecretConfig
El archivo `Secret_Config-sample.py` contiene las variables de configuración para la conexión a la base de datos PostgreSQL. Para configurarlo y que todo funcione correctamente se deben seguir los siguientes pasos:

* 1. Cambia el nombre del archivo a `SecretConfig.py` (Es decir, hay que quitarle el `-sample` al archivo).
* 3. dentro del archivo `SecretConfig.py` pega las credenciales que se copiaron del Neon.tech:
    ```Python
    PGHOST = ' '  # Cambia ' ' por la dirección del host de tu base de datos.
    PGDATABASE = ' '  # Cambia ' ' por el nombre de tu base de datos.
    PGUSER = ' '  # Cambia ' ' por tu nombre de usuario de la base de datos.
    PGPASSWORD = ' '  # Cambia ' ' por tu contraseña de la base de datos.
    PGPORT = '5432'  # Normalmente es '5432' pero si en tu base de datos cambia, pegar el nuevo.

4. Instalar el módulo `psycopg2` para utilizar la app "To Do" con una base de datos PostgreSQL. Para instalarlo ejecuta el siguiente comando en la terminal del proyecto:
    ```
    pip install psycopg2
    ```

5. Instalar el módulo `fpdf ` para poder exportar las tareas en un archivo pdf. Para instalarlo ejecuta el siguiente comando en la terminal del proyecto:
    ```
    pip install fpdf
    ```


## Estructura sugerida

La estructura del proyecto sigue las prácticas recomendadas para mantener un código organizado y modular. A continuación, se describe la estructura sugerida:

- src: Esta carpeta contiene el código fuente de la aplicación. Está organizada en capas para facilitar el mantenimiento y la escalabilidad del proyecto. La estructura de carpetas dentro de src es la siguiente:

* controladores: Contiene el código fuente con la conexión a la base de datos y los querys que se pueden ejecutar dentro de esta.

* model: Contiene el código fuente para modelar los usuarios que se van a ingresar a la base de datos.

* interfaces: Contiene el código fuente de la interfaz, con la cual va a poder interactuar el usuario.


