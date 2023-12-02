import pymysql as ps


def conexion():
    """
    Realiza la conexión la BBDD con los parametros estipulados en el mismo metodo
    :return: No devuelve nada
    """
    try:
        con = ps.connect(host='localhost', port=3307,
                         user='root', password='1234', database='AdrianMoreno_SergioGonzalez')
        cursor = con.cursor()
        return con, cursor

    except Exception as errorConexion:
        print("Error en la conexión:", errorConexion)
        return None, None  # Retorna None en caso de error en la conexión


def confirmarEjecucionCerrarCursor(con, cur):
    """
    Realiza el commit y cierra el cursor
    :param con: Recibe la conexion
    :param cur: Recibe el cursor
    :return: No devuelve nada
    """
    try:
        con.commit()
        cur.close
    except Exception as errorCerrarConexion:
        print("Error al confirmar y cerrar cursor:", errorCerrarConexion)


def crearBBDD():
    """
    Crea la base de datos si no existe
    :return: No devuelve nada
    """
    con, cur = conexion()
    try:
        cur.execute('''CREATE DATABASE IF NOT EXISTS AdrianMoreno_SergioGonzalez;''')
    except Exception as errorCrearBBDD:
        print("Error al crear la base de datos:", errorCrearBBDD)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def crearUsuarioRootBBDD():
    """
    Crea el usuario root si no existe
    :return: No devuelve nada
    """
    con, cur = conexion()
    try:
        cur.execute('''CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '1234';''')
        cur.execute('''GRANT ALL PRIVILEGES ON AdrianMorenoSergioGonzalezCentroDeEstudios.* TO 'root'@'localhost';''')
        cur.execute('''FLUSH PRIVILEGES;''')
    except Exception as errorCrearUsuario:
        print("Error al crear el usuario 'root':", errorCrearUsuario)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def crearUsuarioNuevoBBDD(nombre, contrasena):
    """
    Recibe por parámetros nombre y contraseña y crea un usuario con todos los privilegios.

    :param nombre: Nombre de usuario.
    :param contrasena: Contraseña de usuario.
    :return: No devuelve nada.
    """
    con, cur = conexion()
    try:
        cur.execute(f"CREATE USER IF NOT EXISTS '{nombre}'@'localhost' IDENTIFIED BY '{contrasena}';")
        cur.execute(f"GRANT ALL PRIVILEGES ON AdrianMoreno_SergioGonzalez.* TO '{nombre}'@'localhost';")
        cur.execute("FLUSH PRIVILEGES;")
    except Exception as errorCrearUsuario:
        print(f"Error al crear el usuario '{nombre}': {errorCrearUsuario}")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def crearTablasBBDD():

    """
    Crea las tablas principales de la BBDD si no existen

    :return: No devuelve nada.
    """

    con, cur = conexion()
    try:
            # Tabla para profesores
        cur.execute('''CREATE TABLE IF NOT EXISTS PROFESORES (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            DNI CHAR(9) NOT NULL,
            Nombre VARCHAR(255) NOT NULL,
            Direccion VARCHAR(255) NOT NULL,
            Telefono CHAR(9) NOT NULL
        );''')

        # Tabla para cursos
        cur.execute('''CREATE TABLE IF NOT EXISTS CURSOS (
            Codigo INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255) NOT NULL,
            Descripcion TEXT NOT NULL,
            ProfesorID INT NOT NULL,
            FOREIGN KEY (ProfesorID) REFERENCES PROFESORES (ID)
        );''')

       # Tabla para alumnos
        cur.execute('''CREATE TABLE IF NOT EXISTS ALUMNOS (
            NumeroExpediente INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255) NOT NULL,
            Apellidos VARCHAR(255) NOT NULL,
            Telefono CHAR(9) NOT NULL,
            Direccion VARCHAR(255) NOT NULL,
            FechaNacimiento DATE NOT NULL
        );''')
        #Tabla para la relación entre alumnos y cursos (muchos a muchos)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS AlumnosCursos (
            AlumnoExpediente INT,
            CursoCodigo INT,
            PRIMARY KEY (AlumnoExpediente, CursoCodigo),
            FOREIGN KEY (AlumnoExpediente) REFERENCES ALUMNOS(NumeroExpediente),
            FOREIGN KEY (CursoCodigo) REFERENCES CURSOS(Codigo)
        );''')
    except Exception as errorCrearTablas:
        print("Error al crear las tablas:", errorCrearTablas)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)

def nuevoProfesorInsertBBDD(dni, nombre, direccion, telefono):
    """
    Introduce en la base de datos un nuevo profesor con los datos recibidos por parametro

    :param dni: Recibe DNI profesor
    :param nombre: Recibe nombre profesor
    :param direccion: Recibe direccion profesor
    :param telefono: Recibe telefono profesor
    :return: No devuelve nada
    """
    con, cur = conexion()

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar coches
        cur.execute("insert into PROFESORES(DNI,Nombre,Direccion,Telefono) values (dni, nombre, direccion, telefono)");

    except Exception as errorMeterProfesor:
        print("Error al introducir profesor", errorMeterProfesor)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def mostrarTodosProfesoresBBDD():
    """
    Muestra todos los profesores metidos en la BBDD
    :return: No devuelve nada
    """
    con, cur = conexion()
    try:
        cur.execute("select * from PROFESORES")
        for fila in cur:
            print(fila)
    except Exception as mostrarProfesores:
        print("Error al introducir profesor", mostrarProfesores)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


