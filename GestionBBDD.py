import pymysql as ps
import Utiles as ut
import GestionProfesores as gp
import GestionAlumnos as ga
import GestionCursos as gc
from configparser import ConfigParser


######################################################################
######################################################################
###                             BBDD                               ###
######################################################################
######################################################################

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
    Realiza la conexión la BBDD con los parametros que contiene el fichero de configuracion ConexionConfig.ini
    :return: No devuelve nada
    """

    configuracion = ConfigParser()
    configuracion.read("ConexionConfig.ini")
    try:

        con = ps.connect(host=configuracion.get('conexion', 'host'),
                         port=configuracion.getint('conexion', 'puerto'),
                         user=configuracion.get('conexion', 'user'),
                         db=configuracion.get('conexion' , 'db'),
                         password=configuracion.get('conexion','password'))
        cursor = con.cursor()
        return con, cursor

    except Exception as errorConexionNoExiste:

        try:
            con = ps.connect(host=configuracion.get('conexion', 'host'),
                             port=configuracion.getint('conexion', 'puerto'),
                             user=configuracion.get('conexion', 'user'),
                             password=configuracion.get('conexion','password'))
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
        cur.execute('''CREATE TABLE IF NOT EXISTS profesores (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            DNI CHAR(9) UNIQUE NOT NULL,
            Nombre VARCHAR(255) NOT NULL,
            Direccion VARCHAR(255) NOT NULL,
            Telefono CHAR(9) NOT NULL
        );''')

        # Tabla para cursos
        cur.execute('''CREATE TABLE IF NOT EXISTS cursos (
            Codigo INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255) UNIQUE NOT NULL,
            Descripcion TEXT NOT NULL,
            ProfesorID INT,
            FOREIGN KEY (ProfesorID) REFERENCES profesores (ID) ON DELETE SET NULL
        );''')

        # Tabla para alumnos
        cur.execute('''CREATE TABLE IF NOT EXISTS alumnos (
            NumeroExpediente INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255) NOT NULL,
            Apellidos VARCHAR(255) NOT NULL,
            Telefono CHAR(9) UNIQUE NOT NULL,
            Direccion VARCHAR(255) NOT NULL,
            FechaNacimiento DATE NOT NULL,
            UNIQUE (Nombre, Apellidos)
        );''')
        # Tabla para la relación entre alumnos y cursos (muchos a muchos)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS alumnoscursos (
            AlumnoExpediente INT,
            CursoCodigo INT,
            PRIMARY KEY (AlumnoExpediente, CursoCodigo),
            FOREIGN KEY (AlumnoExpediente) REFERENCES alumnos(NumeroExpediente) ON DELETE CASCADE,
            FOREIGN KEY (CursoCodigo) REFERENCES cursos(Codigo) ON DELETE CASCADE
        );''')
    except Exception as errorCrearTablas:
        print("Error al crear las tablas:", errorCrearTablas)
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


######################################################################
######################################################################
###                          PROFESORES                            ###
######################################################################
######################################################################

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
        # Insertar Profesor
        cur.execute("INSERT INTO profesores (DNI, Nombre, Direccion, Telefono) VALUES (%s, %s, %s, %s)",
                    (dni, nombre, direccion, telefono))
        print("Profesor dado de alta correcctamente")

    except Exception as errorMeterProfesor:
        print("Error al introducir profesor en la BBDD", errorMeterProfesor)
        print("No se ha realizado un nuevo alta")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def eliminarProfesorBBDD():
    """
    Realiza la consulta SQL para eliminar al profesor, pide DNI y confirma
    :return: No devuelve nada
    """
    con, cur = conexion()
    if ut.comprobarVacio("profesores"):
        dni = gp.buscarProfesor()
        if dni != "":
            if ut.confirmacion("Si el profesor imparte algún curso, el curso se quedará sin profesor\nSeguro que quieres ELIMINAR AL PROFESOR?",
                               f"Eliminacion de Profesor con {dni} realizada"):
                try:
                    cur.execute(f"DELETE FROM profesores WHERE DNI = '{dni}'")

                except Exception as errorEliminar:
                    print(f"Error al eliminar el profesor con DNI: {dni}: {errorEliminar}")
                finally:
                    confirmarEjecucionCerrarCursor(con, cur)


def buscarProfesorBBDD(dni):
    """
    Realiza la consulta en la BBDD buscando un profesor, recibiendo el dni
    :param dni: Recibe el DNI
    :return: Devuelve el ID del profesor encontrado por el DNI
    """
    con, cur = conexion()
    encontrado = False
    if ut.comprobarVacio("profesores"):
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
                return profesor[0]
            else:
                print("No se encontró ningún profesor con el DNI especificado.")
                return 0
        except Exception as errorModificarProfesor:
            print(f"Error al buscar el profesor con DNI: {dni}: {errorModificarProfesor}")
            return 0
        finally:
            confirmarEjecucionCerrarCursor(con, cur)

def buscarProfesorBBDDSinPrint(dni):
    """
    Realiza la consulta en la BBDD buscando un profesor, recibiendo el dni
    :param dni: Recibe el DNI
    :return: Devuelve el ID del profesor encontrado por el DNI
    """
    con, cur = conexion()
    encontrado = False

    try:
        cur.execute(f"SELECT * FROM profesores WHERE DNI = '{dni}'")
        profesor = cur.fetchone()
        if profesor:
            return profesor[0]
        else:
            print("No se encontró ningún profesor con el DNI especificado.")
            return 0
    except Exception as errorModificarProfesor:
        print(f"Error al buscar el profesor con DNI: {dni}: {errorModificarProfesor}")
        return 0
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def modificarProfesorBBDD():
    """
    Permite al usuario modificar un profesor seleccionando el campo a modificar.
    :return: No devuelve nada.
    """
    con, cur = conexion()
    if ut.comprobarVacio("profesores"):
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

                    while not finEntradaAlta and fallos < 5:
                        dniNuevo = input("DNI: ").strip().upper()
                        if ut.validarDNI(dniNuevo):
                            if buscarProfesorBBDDSinPrint(dniNuevo) == 0:
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(f"UPDATE profesores SET DNI = '{dniNuevo}' WHERE DNI = '{dni}'")
                                    finEntradaAlta = True
                                    print("Profesor actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                fallos = ut.fallo(fallos, "DNI está ya en la BBDD")
                        else:
                            fallos = ut.fallo(fallos, "El Dni debe tener 8 numeros y una letra")

                elif opcion == "2":

                    while not finEntradaAlta and fallos < 5:

                        nombreNuevo = input("Nombre: ").strip().upper()
                        if ut.validarNombre(nombreNuevo):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(f"UPDATE profesores SET Nombre = '{nombreNuevo}' WHERE DNI = '{dni}'")
                                finEntradaAlta = True
                                print("Profesor actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")

                elif opcion == "3":

                    while not finEntradaAlta and fallos < 5:
                        direccionNueva = input("Direccion: ").strip().upper()
                        if ut.validarDireccion(direccionNueva):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(f"UPDATE profesores SET Direccion = '{direccionNueva}' WHERE DNI = '{dni}'")
                                finEntradaAlta = True
                                print("Profesor actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

                elif opcion == "4":

                    while not finEntradaAlta and fallos < 5:
                        telefonoNuevo = input("Telefono: ").strip().upper()
                        if ut.validarTelefono(telefonoNuevo):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(f"UPDATE profesores SET Telefono = '{telefonoNuevo}' WHERE DNI = '{dni}'")
                                finEntradaAlta = True
                                print("Profesor actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos, "El Telefono debe tener 9 numeros")

                elif opcion == "0":
                    print("Modificación cancelada.")
                else:
                    print("Opción no válida.")

            except Exception as errorModificarProfesor:
                print(f"Error al modificar el profesor {dni}: {errorModificarProfesor}")
            finally:
                confirmarEjecucionCerrarCursor(con, cur)


def mostrarProfesores():
    """
    Muestra los profesores de una manera atractiva
    :return: No devuelve nada
    """
    con, cur = conexion()
    cont = 1
    # Seleccionar todos los alumnos
    cur.execute("SELECT * FROM profesores")
    # Recuperar todos los resultados
    profesores = cur.fetchall()
    if not profesores:
        print("No hay profesores registrados en la BBDD.")
    else:
        print("Lista de profesores:")
        for profesor in profesores:
            print(f"--- PROFESOR {cont}---")
            print("ID:", profesor[0])
            print("Dni:", profesor[1])
            print("Nombre:", profesor[2])
            print("Direccion:", profesor[3])
            print("Telefono:", profesor[4], '\n')
            cont = cont + 1
    confirmarEjecucionCerrarCursor(con, cur)


######################################################################
######################################################################
###                           CURSOS                               ###
######################################################################
######################################################################

def nuevoCursoInsertBBDD(nombre, descripcion):
    """
    Introduce en la base de datos un nuevo profesor con los datos recibidos por parametro
    :param nombre: Recibe nombre Curso
    :param descripcion: Recibe descripcion Curso
    :return: No devuelve nada
    """
    con, cur = conexion()

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar cursos
        cur.execute("INSERT INTO cursos (Nombre, Descripcion) VALUES (%s, %s)", (nombre, descripcion))
        print("Curso dado de alta correcctamente")

    except Exception as errorMeterProfesor:
        print("Error al introducir Curso en la BBDD", errorMeterProfesor)
        print("No se ha realizado un nuevo alta")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def eliminarCursosBBDD():
    '''
    Metodo para eliminar un curso
    :return: No devuelve nada
    '''
    con, cur = conexion()
    if ut.comprobarVacio("cursos"):
        nombre = gc.buscarCurso()

        if nombre != "":
            if ut.confirmacion("Si el curso tiene alumnos, estos de desmatricularan\nSeguro que quieres ELIMINAR EL CURSO?", f"Eliminacion del CURSO: {nombre} realizada"):
                try:
                    cur.execute(f"DELETE FROM cursos WHERE Nombre = '{nombre}'")

                except Exception as errorEliminar:
                    print(f"Error al eliminar el CURSO: {nombre}: {errorEliminar}")
                finally:
                    confirmarEjecucionCerrarCursor(con, cur)


def buscarCursoBBDD(nombre):
    '''
    Metodo para buscar un curso concreto , tambien muestra su profesor si tiene uno
    , en caso contrario avisa de que todavia no tiene
    :param nombre: Nombre del curso que se desea buscar
    :return: Devuelve True o False en funcion de si encuentra el curso con el nombre indicado
    '''
    con, cur = conexion()
    encontrado = False
    if ut.comprobarVacio("cursos"):
        try:
            cur.execute(f"SELECT * FROM cursos WHERE Nombre = '{nombre}'")
            curso = cur.fetchone()
            if curso:
                print("Datos del Curso:")
                print("Codigo:", curso[0])
                print("Nombre:", curso[1])
                print("Descripcion:", curso[2])
                cur.execute(f''' SELECT profesores.Nombre , profesores.DNI 
                            from profesores 
                            JOIN cursos ON profesores.ID = cursos.ProfesorID 
                            WHERE cursos.Codigo = '{curso[0]}' ''')
                profe = cur.fetchone()
                if profe is not None:
                    print(f"Profesor: {profe[0]} , con el DNI: {profe[1]}\n")
                else:
                    print("Todavia no tiene ningun profesor asignado\n")
                encontrado = True
            else:
                print("No se encontro ningún curso con el nombre especificado.")
        except Exception as errorModificarProfesor:
            print(f"Error al buscar el curso con nombre: {nombre}: {errorModificarProfesor}")
        finally:
            confirmarEjecucionCerrarCursor(con, cur)
            return encontrado


def modificarCursoBBDD():
    """
    Permite al usuario modificar un profesor seleccionando el campo a modificar.

    :return: No devuelve nada.
    """
    con, cur = conexion()
    if ut.comprobarVacio("cursos"):
        nombre = gc.buscarCurso()
        if nombre != "":
            try:
                # Consultar datos actuales del profesor
                cur.execute(f"SELECT * FROM cursos WHERE Nombre = '{nombre}'")
                profesor_actual = cur.fetchone()

                # Mostrar opciones al usuario
                print("\nSeleccione el campo a modificar:")
                print("1. Nombre")
                print("2. Descripcion")
                print("3. Aniadir/Cambiar Profesor de Curso")
                print("0. Cancelar")

                finEntradaAlta = False
                fallos = 0

                opcion = input("Opción: ")

                if opcion == "1":

                    while not finEntradaAlta and fallos < 5:

                        nombreNuevo = input("Nombre: ").strip().upper()
                        if ut.validarNombre(nombreNuevo):
                            if devolverIddeCurso(nombreNuevo) is None:
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(f"UPDATE cursos SET Nombre = '{nombreNuevo}' WHERE Nombre = '{nombre}'")
                                    finEntradaAlta = True
                                    print("Curso actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                fallos = ut.fallo(fallos, "El nombre ya esta en la BBDD.")
                        else:
                            fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")

                elif opcion == "2":

                    while not finEntradaAlta and fallos < 5:
                        descripcionNueva = input("Descripcion: ").strip().upper()
                        if ut.validarDireccion(descripcionNueva):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(
                                    f"UPDATE cursos SET Descripcion = '{descripcionNueva}' WHERE Nombre = '{nombre}'")
                                finEntradaAlta = True
                                print("Curso actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

                elif opcion == "3":

                    while not finEntradaAlta and fallos < 5:
                        profesorDni = input("DNI Profesor: ").strip().upper()

                        if ut.validarDNI(profesorDni):
                            IDProfesor = buscarProfesorBBDD(profesorDni)
                            if IDProfesor != 0:
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(
                                        f"UPDATE cursos SET ProfesorID = '{IDProfesor}' WHERE Nombre = '{nombre}'")
                                    finEntradaAlta = True
                                    print("Curso actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                print("No hay en la BBDD ningun profesor con ese DNI")
                        else:
                            fallos = ut.fallo(fallos, "El DNI debe de tener 8 digitos y una letra")

                elif opcion == "0":
                    print("Modificación cancelada.")
                else:
                    print("Opción no válida.")


            except Exception as errorModificarProfesor:
                print(f"Error al modificar el profesor {nombre}: {errorModificarProfesor}")
            finally:
                confirmarEjecucionCerrarCursor(con, cur)


def mostrarTodosCursosBBDD():
    '''
    Metodo para mostrar todos los cursos y en caso de tener un profesor asignado lo muestra tambien
    :return: No devuelve nada
    '''
    con, cur = conexion()
    cont = 1
    # Seleccionar todos los cursos
    cur.execute("SELECT * FROM cursos")
    # Recuperar todos los resultados
    cursos = cur.fetchall()
    if not cursos:
        print("No hay cursos registrados en la BBDD.")
    else:
        print("Lista de cursos:")
        for curso in cursos:
            print(f"--- CURSO {cont}---")
            print("Codigo:", curso[0])
            print("Nombre:", curso[1])
            print("Descripcion:", curso[2])
            cur.execute(f''' SELECT profesores.Nombre , profesores.DNI 
            from profesores 
            JOIN cursos ON profesores.ID = cursos.ProfesorID 
            WHERE cursos.Codigo = '{curso[0]}' ''')
            profe = cur.fetchone()
            if profe is not None:
                print(f"Profesor: {profe[0]} , con el DNI: {profe[1]}\n")
            else:
                print("")

            cont = cont + 1
    confirmarEjecucionCerrarCursor(con, cur)


def devolverIddeCurso(nombre):
    '''
    Metodo para devolver el id del curso con el nombre pasado por parametro
    :param nombre: Nombre del curso del que se desea saber el id
    :return: Devuelve el id si encuentra el curso , de lo contrario devuelve None
    '''

    con, cur = conexion()

    cur.execute(f"select * from cursos WHERE Nombre = '{nombre}'")
    curso = cur.fetchone()

    if curso is not None:
        # El resultado no es None, lo que significa que se encontró un curso con ese nombre
        id = curso[0]
        return id


    confirmarEjecucionCerrarCursor(con, cur)


######################################################################
######################################################################
###                           ALUMNOS                              ###
######################################################################
######################################################################
def nuevoAlumnoInsertBBDD(nombre, apellidos, telefono, direccion, fecha):
    '''
    Metodo para inertar nuevos alumnos a la bbdd el cual recibe todos los atributos necesarios
    :param nombre: Nombre del nuevo alumno
    :param apellidos: apellidos del nuevo alumno
    :param telefono: telefono del nuevo alumno
    :param direccion: direccion del nuevo alumno
    :param fecha: fecha del nuevo alumno
    :return: No devuelve nada
    '''
    con, cur = conexion()

    try:
        cur.execute(
            f"INSERT INTO alumnos (Nombre, Apellidos, Telefono, Direccion, FechaNacimiento) VALUES ('{nombre}', '{apellidos}', '{telefono}', '{direccion}', '{fecha}');")
        print("Alumno dado de alta correcctamente")

    except Exception as errorMeterProfesor:
        print("Error al introducir alumno en la BBDD", errorMeterProfesor)
        print("No se ha realizado un nuevo alta")
    finally:
        confirmarEjecucionCerrarCursor(con, cur)


def buscarAlumnoBBDD(nombre, apellidos):
    '''
    Metodo para buscar un alumno , tambien imprime la informacion de este en caso de encontrarlo
    :param nombre: Nombre del alumno a buscar
    :param apellidos: Apellidos del alumno a buscar
    :return: Devuelve el id o 0 en caso de no encontrar el alumno
    '''
    con, cur = conexion()
    encontrado = False
    if ut.comprobarVacio("alumnos"):
        try:
            cur.execute(f"SELECT * FROM alumnos WHERE Nombre = '{nombre}' AND Apellidos ='{apellidos}'")
            alumno = cur.fetchone()
            if alumno:
                print("Datos del Alumno:")
                print("ID:", alumno[0])
                print("Nombre:", alumno[1])
                print("Apellidos:", alumno[2])
                print("telefono:", alumno[3])
                print("Direccion:", alumno[4])
                print("Fecha de nacimiento :", alumno[5])
                return alumno[0]
            else:
                print("No se encontro ningun alumno ")
                return 0
        except:
            print("Error al buscar el alumno con ")
            return 0
        finally:
            confirmarEjecucionCerrarCursor(con, cur)


def buscarAlumnoBBDDid(nombre, apellidos):
    '''
    Metodo para buscar un alumno
    :param nombre: Nombre del alumno a buscar
    :param apellidos: Apellidos del alumno a buscar
    :return: Devuelve el id o 0 en caso de no encontrar el alumno
    '''
    con, cur = conexion()
    encontrado = False
    if ut.comprobarVacio("alumnos"):
        try:
            cur.execute(f"SELECT * FROM alumnos WHERE Nombre = '{nombre}' AND Apellidos ='{apellidos}'")
            alumno = cur.fetchone()
            if alumno:
                return alumno[0]
            else:
                print("No se encontro ningun alumno. ")
                return 0
        except:
            print("Error al buscar el alumno. ")
            return 0
        finally:
            confirmarEjecucionCerrarCursor(con, cur)


def eliminarAlumnoBBDD():
    '''
    Metodo para eliminar un alumno de la bbdd
    :return: No devuelve nada
    '''
    con, cur = conexion()
    if ut.comprobarVacio("alumnos"):
        nombre = ga.buscarAlumno()
        if nombre != "":
            if ut.confirmacion("Seguro que quieres eliminar el Alumno?",
                               f"Eliminacion del Alumno {nombre[0]} {nombre[1]}"):
                try:
                    cur.execute(f"DELETE FROM alumnos WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")

                except Exception as errorEliminar:
                    print(f"Error al eliminar el Alumno: {nombre[0]}")
                finally:
                    confirmarEjecucionCerrarCursor(con, cur)

def modificarAlumnoBBDD():
    '''
    Permite al usuario modificar un Alumno seleccionando el campo a modificar
    :return: No devuelve nada
    '''
    con, cur = conexion()
    if ut.comprobarVacio("alumnos"):
        nombre = ga.buscarAlumno()
        if nombre != "":
            try:
                # Consultar datos actuales del profesor
                cur.execute(f"SELECT * FROM alumnos WHERE Nombre = '{nombre[0]}'")
                alumnoAlumno = cur.fetchone()

                # Mostrar opciones al usuario
                print("\nSeleccione el campo a modificar:")
                print("1. Nombre")
                print("2. Apellidos")
                print("3. Telefono")
                print("4. Direccion")
                print("5. Fecha de Nacimiento")
                print("0. Cancelar")

                finEntradaAlta = False
                fallos = 0

                opcion = input("Opcion: ")

                if opcion == "1":

                    while not finEntradaAlta and fallos < 5:
                        nombreNuevo = input("Nuevo nombre: ").strip().upper()
                        if ut.validarNombre(nombreNuevo):
                            if not ga.alumnoRepe(nombreNuevo, nombre[1]):
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(f"UPDATE alumnos SET Nombre = '{nombreNuevo}' WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")
                                    finEntradaAlta = True
                                    print("Alumno actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                fallos = ut.fallo(fallos,f"Ya existe un alumno con el nombre {nombreNuevo} y el apellido {nombre[1]}")
                        else:
                            fallos = ut.fallo(fallos, "El nombre debe tener minimo dos caracteres")

                elif opcion == "2":

                    while not finEntradaAlta and fallos < 5:

                        nuevoApellidos = input("Nuevos apellidos: ").strip().upper()
                        if ut.validarNombre(nuevoApellidos):
                            if not ga.alumnoRepe(nombre[0], nuevoApellidos):
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(f"UPDATE alumnos SET Apellidos = '{nuevoApellidos}' WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")
                                    finEntradaAlta = True
                                    print("Alumno actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                fallos = ut.fallo(fallos,f"Ya existe un alumno con el nombre {nombre[0]} y el apellido {nuevoApellidos}")
                        else:
                            fallos = ut.fallo(fallos, "Los apellidos deben contener al menos 2 caracteres.")

                elif opcion == "4":

                    while not finEntradaAlta and fallos < 5:
                        direccionNueva = input("Nueva direccion: ").strip().upper()
                        if ut.validarDireccion(direccionNueva):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(f"UPDATE alumnos SET Direccion = '{direccionNueva}' WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")
                                finEntradaAlta = True
                                print("Alumno actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

                elif opcion == "3":

                    while not finEntradaAlta and fallos < 5:
                        telefonoNuevo = input("Nuevo telefono: ").strip().upper()
                        if ut.validarTelefono(telefonoNuevo):
                            if not ga.tlfRepe(telefonoNuevo):
                                if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                    cur.execute(f"UPDATE alumnos SET Telefono = '{telefonoNuevo}' WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")
                                    finEntradaAlta = True
                                    print("Alumno actualizado correctamente.")
                                else:
                                    finEntradaAlta=True
                            else:
                                fallos = ut.fallo(fallos, "El telefono introducido ya existe en otro alumno.")
                        else:
                            fallos = ut.fallo(fallos, "El Telefono debe tener 9 numeros")
                elif opcion == "5":

                    while not finEntradaAlta and fallos < 5:
                        fechaNueva = input("Nueva fecha de nacimiento: ").strip().upper()
                        if ut.validarFechaNacimiento(fechaNueva):
                            if ut.confirmacion("Seguro que quieres modificar?", "Solicitud"):
                                cur.execute(f"UPDATE alumnos SET FechaNacimiento = '{fechaNueva}' WHERE Nombre = '{nombre[0]}' AND Apellidos = '{nombre[1]}'")
                                finEntradaAlta = True
                                print("Alumno actualizado correctamente.")
                            else:
                                finEntradaAlta = True
                        else:
                            fallos = ut.fallo(fallos,"Fecha no valida ,deben ser numeros con el siguiente formato: yyyy-mm-dd.\n Además debe ser entre 1950 y 2020")
                elif opcion == "0":
                    print("Modificación cancelada.")
                else:
                    print("Opción no válida.")



            except Exception as errorModificarProfesor:
                print(f"Error al modificar el alumno {nombre[0]} {nombre[1]}")
            finally:
                confirmarEjecucionCerrarCursor(con, cur)

def mostrarAlumnos():
    '''
    Metodo para mostrar todos los amlumnos (y su informacion) de la base de datos
    :return: No devuelve nada
    '''
    con, cur = conexion()
    cont = 1
    # Seleccionar todos los alumnos
    cur.execute("SELECT * FROM alumnos")
    # Recuperar todos los resultados
    alumnos = cur.fetchall()
    if not alumnos:
        print("No hay alumnos registrados en la BBDD.")
    else:
        print("Lista de alumnos:")
        for alumno in alumnos:
            print(f"--- Alumno {cont}---")
            print("Numero de Expediente:", alumno[0])
            print("Nombre:", alumno[1])
            print("Apellidos:", alumno[2])
            print("Telefono:", alumno[3])
            print("Direccion:", alumno[4])
            print("Fecha de Nacimiento:", alumno[5], '\n')
            cont = cont + 1
    confirmarEjecucionCerrarCursor(con, cur)


def matricularAlumno():
    '''
    Metodo para dar de alta un alumno en un curso , comprueba si el alumno ya se encuentra en el curso deseado
    :return: No devuelve nada
    '''
    con, cur = conexion()
    encontrado = False
    fallos = 0
    if ut.comprobarVacio("alumnos"):
        if ut.comprobarVacio("cursos"):
            while not encontrado and fallos < 5:
                nombreC = input("Nombre del curso: ").strip().upper()
                idCurs = devolverIddeCurso(nombreC)
                if idCurs is not None:
                    encontrado = True
                    print("Curso encontrado")
                else:
                    fallos = ut.fallo(fallos, "Curso no encontrado")
            if fallos < 5:
                encontrado = False
                fallos = 0
                while not encontrado and fallos < 5:

                    alumnoM = ga.buscarAlumno()
                    if alumnoM != "":
                        encontrado = True
                        print("Alumno encontrado")
                    else:
                        fallos = ut.fallo(fallos, "Alumno no encontrado")

            if fallos < 5:

                op = ut.confirmacion(
                    f"Seguro que deseas dar de alta al alumno {alumnoM[0]} {alumnoM[1]} al curso {nombreC} ?", "Matricula ")
                if op:
                    idAlumnoM = buscarAlumnoBBDDid(alumnoM[0], alumnoM[1])

                    cur.execute(f''' SELECT * FROM alumnoscursos 
                    WHERE AlumnoExpediente = '{idAlumnoM}' AND CursoCodigo = '{idCurs}' ''')
                    alumnoEnCurso = cur.fetchone()
                    if alumnoEnCurso is None:
                        cur.execute(
                            f"INSERT INTO alumnoscursos (AlumnoExpediente, CursoCodigo) VALUES ('{idAlumnoM}', '{idCurs}');")
                        print("Alumno matriculado correctamente.")
                    else:
                        print("No se matriculo el alumno , ya pertenece a este Curso.")
    confirmarEjecucionCerrarCursor(con, cur)

def desmatricularAlumno():
    """
    Metodo para dar de baja un alumno en un curso.
    :return: No devuelve nada
    """
    con, cur = conexion()
    encontrado = False
    fallos = 0
    if ut.comprobarVacio("alumnos"):
        if ut.comprobarVacio("cursos"):
            while not encontrado and fallos < 5:
                nombreC = input("Nombre del curso: ").strip().upper()
                idCurs = devolverIddeCurso(nombreC)
                if idCurs is not None:
                    encontrado = True
                    print("Curso encontrado")
                else:
                    fallos = ut.fallo(fallos, "Curso no encontrado")
            encontrado = False
            fallos = 0
            if fallos < 5:
                while not encontrado and fallos < 5:
                    cur.execute(f'''SELECT NumeroExpediente, Nombre, Apellidos FROM alumnos JOIN alumnoscursos on alumnos.NumeroExpediente = alumnoscursos.AlumnoExpediente where CursoCodigo = '{idCurs}' ''')
                    alumnos = cur.fetchall()
                    print("Lista de alumnos:")
                    for alumno in alumnos:
                        print(f"--- Alumno ---")
                        print("Numero de Expediente:", alumno[0])
                        print("Nombre:", alumno[1])
                        print("Apellidos:", alumno[2], '\n')

                    if alumnos is not None:
                        encontrado = True
                        print("Alumno encontrado")
                    else:
                        fallos = ut.fallo(fallos, "Alumno no encontrado")

            if fallos < 5:
                expAlumno = input("Introduce el Numero de Expediente  del alumno a Eliminar: ")
                cur.execute(f'''SELECT * FROM alumnoscursos WHERE AlumnoExpediente = '{expAlumno}' ''')
                compAl = cur.fetchone()
                if compAl is not None:
                    op = ut.confirmacion(
                        f"Seguro que deseas dar de baja al alumno del curso {nombreC} ?",
                        "Desmatriculacion ")
                    if op:
                        cur.execute(f'''DELETE FROM alumnoscursos WHERE AlumnoExpediente = '{expAlumno}' ''')
                else:
                    print("No has introducido un expediente correcto")
    confirmarEjecucionCerrarCursor(con, cur)

def mostrarAlumnosdeCurso():
    '''
    Metodo para mostrar todos los alumnos que se encuentren dentro de un mismo curso
    :return: No devuelve nada
    '''
    con, cur = conexion()
    encontrado = False
    fallos = 0
    if ut.comprobarVacio("cursos"):
        if ut.comprobarVacio("alumnos"):
            while not encontrado and fallos < 5:
                nombreC = input("Nombre del curso: ").strip().upper()
                idCurs = devolverIddeCurso(nombreC)
                if idCurs is not None:
                    encontrado = True
                    print("Curso encontrado")
                else:
                    fallos = ut.fallo(fallos, "Curso no encontrado")
            if fallos < 5:
                cur.execute(f'''SELECT NumeroExpediente , nombre , apellidos 
                FROM alumnos 
                JOIN alumnoscursos 
                ON alumnoscursos.AlumnoExpediente = alumnos.NumeroExpediente 
                WHERE alumnoscursos.CursoCodigo = {idCurs}''')

                alumnos = cur.fetchall()
                for alumno in alumnos:
                    print(f"Numero de Expediente: {alumno[0]} , Alumno: {alumno[1]} {alumno[2]}\n")
    confirmarEjecucionCerrarCursor(con, cur)
