import pymysql as ps
import Utiles as ut
import GestionProfesores as gp
def crearBBDD():
    """
    Crea la base de datos si no existe
    :return: No devuelve nada
    """
    con, cur = conexion()
    try:
        cur.execute('CREATE DATABASE IF NOT EXISTS adrianmoreno_sergiogonzalez;')
    except Exception as errorCrearBBDD:
        print("Error al crear la base de datos:", errorCrearBBDD)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)

def conexion():
    """
    Realiza la conexión la BBDD con los parametros estipulados en el mismo metodo
    :return: No devuelve nada
    """
    try:
        con = ps.connect(host='localhost', port=3306,
                         user='root', password='1234', database='adrianmoreno_sergiogonzalez')
        cursor = con.cursor()
        return con, cursor

    except Exception as errorConexionNoExiste:

        try:
            con = ps.connect(host='localhost', port=3306,
                             user='root', password='1234')
            cursor = con.cursor()
            print("La BBDD no existe, se creará")
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
        cur.close()
    except Exception as errorCerrarConexion:
        print("Error al confirmar y cerrar cursor:", errorCerrarConexion)


def crearUsuarioRootBBDD():
    """
    Crea el usuario root si no existe
    :return: No devuelve nada
    """
    con, cur = conexion()
    try:
        cur.execute('''CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '1234';''')
        cur.execute('''GRANT ALL PRIVILEGES ON adrianmoreno_sergiogonzalez.* TO 'root'@'localhost';''')
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
        cur.execute(f"GRANT ALL PRIVILEGES ON adrianmoreno_sergiogonzalez.* TO '{nombre}'@'localhost';")
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
            DNI CHAR(9) UNIQUE NOT NULL,
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
        cur.execute("INSERT INTO profesores (DNI, Nombre, Direccion, Telefono) VALUES (%s, %s, %s, %s)", (dni, nombre, direccion, telefono))
        print("Profesor dado de alta correcctamente")

    except Exception as errorMeterProfesor:
        print("Error al introducir profesor en la BBDD", errorMeterProfesor)
        print("No se ha realizado un nuevo alta")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)

def eliminarProfesorBBDD():

    con, cur = conexion()
    dni = gp.buscarProfesor()
    if dni != "":
        if ut.confirmacion("Seguro que quieres ELIMINAR AL PROFESOR?", f"Eliminacion de Profesor con {dni} realizada"):
            try:
                cur.execute(f"DELETE FROM profesores WHERE DNI = '{dni}'")

            except Exception as errorEliminar:
                print(f"Error al eliminar el profesor con DNI: {dni}: {errorEliminar}")
            finally:
                confirmarEjecucionCerrarCursor(con, cur)



def buscarProfesorBBDD(dni):
    con, cur = conexion()
    encontrado = False
    try:
        cur.execute(f"SELECT * FROM profesores WHERE DNI = '{dni}'")
        profesor = cur.fetchone()
        if profesor:
            print("Datos del profesor:")
            print("ID:", profesor[0])
            print("DNI:", profesor[1])
            print("Nombre:", profesor[2])
            print("Dirección:", profesor[3])
            print("Teléfono:", profesor[4])
            encontrado = True
        else:
            print("No se encontró ningún profesor con el DNI especificado.")
    except Exception as errorModificarProfesor:
        print(f"Error al buscar el profesor con DNI: {dni}: {errorModificarProfesor}")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)
        return encontrado


def modificarProfesorBBDD():
    """
    Permite al usuario modificar un profesor seleccionando el campo a modificar.

    :param dni: ID del profesor a modificar.
    :return: No devuelve nada.
    """
    con, cur = conexion()
    dni = gp.buscarProfesor()
    if dni != "":
        try:
            # Consultar datos actuales del profesor
            cur.execute(f"SELECT * FROM PROFESORES WHERE ID = '{dni}'")
            profesor_actual = cur.fetchone()


            # Mostrar opciones al usuario
            print("\nSeleccione el campo a modificar:")
            print("1. DNI")
            print("2. Nombre")
            print("3. Dirección")
            print("4. Teléfono")
            print("0. Cancelar")

            finEntradaAlta = False
            fallos = 0

            opcion = input("Opción: ")

            if opcion == "1":

                while not finEntradaAlta and fallos < 3:
                    dniNuevo = input("DNI: ").strip().upper()
                    if ut.validarDNI(dniNuevo):
                        if ut.confirmacion("Seguro que quieres modificar?", "DNI"):
                            cur.execute(f"UPDATE profesores SET DNI = '{dniNuevo}' WHERE DNI = '{dni}'")
                            finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "El Dni debe tener 8 numeros y una letra")

            elif opcion == "2":

                while not finEntradaAlta and fallos < 3:

                    nombreNuevo = input("Nombre: ").strip().upper()
                    if ut.validarNombre(nombreNuevo):
                        if ut.confirmacion("Seguro que quieres modificar?", "NOMBRE"):
                            cur.execute(f"UPDATE profesores SET Nombre = '{nombreNuevo}' WHERE DNI = '{dni}'")
                            finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")

            elif opcion == "3":

                while not finEntradaAlta and fallos < 3:
                    direccionNueva = input("Direccion: ").strip().upper()
                    if ut.validarDireccion(direccionNueva):
                        if ut.confirmacion("Seguro que quieres modificar?", "DIRECCION"):
                            cur.execute(f"UPDATE profesores SET Direccion = '{direccionNueva}' WHERE DNI = '{dni}'")
                            finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

            elif opcion == "4":

                while not finEntradaAlta and fallos < 3:
                    telefonoNuevo = input("Nombre: ").strip().upper()
                    if ut.validarTelefono(telefonoNuevo):
                        if ut.confirmacion("Seguro que quieres modificar?", "DNI"):
                            cur.execute(f"UPDATE profesores SET Telefono = '{telefonoNuevo}' WHERE DNI = '{dni}'")
                            finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "El Telefono debe tener 9 numeros")

            elif opcion == "0":
                print("Modificación cancelada.")
            else:
                print("Opción no válida.")

            print("Profesor actualizado correctamente.")



        except Exception as errorModificarProfesor:
            print(f"Error al modificar el profesor {dni}: {errorModificarProfesor}")
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


