import pymysql as ps


def conexion():
    con = ps.connect(host='localhost', port=3307,
                     user='root', password='1234', database='AdrianMoreno_SergioGonzalez')

    cursor = con.cursor()
    return con, cursor

def confirmarEjecucionCerrarConexion(con, cur):
    con.commit()
    cur.close


def crearBBDD():
    "CREATE DATABASE IF NOT EXISTS AdrianMoreno_SergioGonzalez;"

def crearUsuarioRoot(cur):
    cur.execute('''CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '1234';''')
    cur.execute('''GRANT ALL PRIVILEGES ON AdrianMorenoSergioGonzalezCentroDeEstudios.* TO 'root'@'localhost';''')
    "FLUSH PRIVILEGES;"

def crearTablasBBDD():

    con, cur = conexion()

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

def nuevoProfesorInsertBBDD(dni, nombre, direccion, telefono):

    con, cur = conexion()

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar coches
        cur.execute("insert into PROFESORES(DNI,Nombre,Direccion,Telefono) values (dni, nombre, direccion, telefono)");

    except Exception as errorMeterProfesor:
        print("Error al introducir coches", errorMeterProfesor)

    confirmarEjecucionCerrarConexion(con, cur)




def mostrarTodosProfesoresBBDD():
    con, cur = conexion()

    cur.execute("select * from PROFESORES")
    for fila in cur:
        print(fila)

    confirmarEjecucionCerrarConexion(con, cur)


