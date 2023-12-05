import pymysql as ps


def crearBD(cur):

    cur.execute('''CREATE TABLE IF NOT EXISTS COCHES (
                              codigo INT auto_increment primary key,
                              marca VARCHAR(50),
                              modelo VARCHAR(50),
                              color VARCHAR(50),
                              precio REAL);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS clientes (
                              codigo INT auto_increment primary key,
                              dni char(9) UNIQUE,
                              nombre text
                            );''')

    cur.execute('''CREATE TABLE IF NOT EXISTS alquileres (
                              codigo INT auto_increment primary key,
                              codCliente INT NOT NULL,
                              codCoche INT NOT NULL,
                              dias INT,
                              precio real,
                              FOREIGN KEY(codCliente) REFERENCES clientes(codigo),
                              FOREIGN KEY(codCoche) REFERENCES COCHES(codigo)
                            );''')
    con.commit()



def insertarFilas(cur):

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar coches
        cur.execute("insert into COCHES(modelo,marca,precio) values ('Ferrari', 'Uno', 1000)");
        cur.execute("insert into COCHES(modelo,marca,precio) values ('Mercedes', 'Benz', 500)");
        cur.execute("insert into COCHES(modelo,marca,precio) values ('Fiat', 'Tipo', 250)");
    except Exception as errorCoches:
        print("Error al introducir coches", errorCoches)

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar clientes
        cur.execute("insert into clientes(dni,nombre) values ('74185296e', 'Eusebio')");
        cur.execute("insert into clientes(dni,nombre) values ('74654656A', 'PACO')");
        cur.execute("insert into clientes(dni,nombre) values ('74185SDFT', 'SERGIO')");
    except Exception as errorClientes:
        print("Error al introducir clientes", errorClientes)

    try:
        cur.execute("set FOREIGN_KEY_CHECKS = 1")
        # Insertar alquileres
        cur.execute("insert into alquileres(codCliente,codCoche,dias,precio) values (1, 2, 5, 3000)");
        cur.execute("insert into alquileres(codCliente,codCoche,dias,precio) values (2, 3, 10, 500)");
        cur.execute("insert into alquileres(codCliente,codCoche,dias,precio) values (3, 1, 20, 1000)");

    except Exception as errorAlquileres:
        print("Error al introducir alquileres", errorAlquileres)

    con.commit()
    cur.close


def mostrarTablas(cur):

    cur.execute("select * from COCHES")
    for fila in cur:
        print(fila)
    cur.execute("select * from clientes")
    for fila in cur:
        print(fila)
    cur.execute("select * from alquileres")
    for fila in cur:
        print(fila)
    con.commit()
    cur.close


def eliminarRegistros(con):
    cur = con.cursor()
    cur.execute("delete from alquileres")
    cur.execute("delete from clientes")
    cur.execute("delete from coches")
    con.commit()
    cur.close


con = ps.connect(host='localhost', port=3307,
                 user='root', password='montero', database='PruebaJoin')

cursor = con.cursor()
cursor.execute("select @@version")
output = cursor.fetchall()

print(output)

cursor.execute("use PruebaJoin")

crearBD(cursor)

insertarFilas(cursor)
mostrarTablas(cursor)
# eliminarRegistros(conexion)

# opcion = input("Inserta una opcion:\n1. Introducir coches\n2. Introducir Cliente\3.Hacer un alquiler")

# Insertar filas en una tabla


