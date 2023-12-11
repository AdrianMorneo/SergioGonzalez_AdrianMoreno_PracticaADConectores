
from datetime import datetime
import GestionBBDD as gbd
'''
Levantar servicio docker o cualquier otro desde el ubuntu... 
1- En la power shell de Windows introducir el comando → wsl
2-Una vez dentro del ubuntu introducir el comando → docker service start
Para comprobar que funciona
Introducir el comando →service docker status
Para ver los contenedores y sus datos generales 
Introducir el comando → docker ps -a
Para levantar/activar un contenedor
Introducir el comando → docker start " id del contenedor (Con los primeros caracteres vale )"
Comprobar la correcta conexión con el cliente MariaDB
1-Meterte en el cmd desde el bin de xammp e Introducir el comando → mysql -u root -p -P3307
2-Meter contraseña predeterminada en mi caso (my-secret-pw)
3- Introducir el comando → show databases;
'''
def validarDNI(dni):
    # Validar DNI con 8 números y una letra al final
    """
    Comprueba que un DNI tenga el formato correcto
    :param dni: El DNI a validar
    :return: Devuelve si es correcto o no
    """
    return len(dni) == 9 and dni[:-1].isdigit() and dni[-1].isalpha()


def validarNombre(nombre):
    # Validar que el nombre tenga más de 2 caracteres
    """
    Comprueba que un nombre tenga al menos 2 caracteres
    :param nombre: EL nombre a validar
    :return: Si se cumple o no
    """
    return len(nombre) > 1

def validarDireccion(direccion):
    # Validar que la dirección tenga más de 4 caracteres
    """
    Comprueba que la direccion tenga al menos 4 caracteres
    :param direccion: EL nombre a validar
    :return: Si se cumple o no
    """
    return len(direccion) > 3

def validarTelefono(telefono):
    # Validar que el teléfono tenga 9 números
    """
    Metodo para validar el formato de un numero telefono
    :param telefono:
    :return:
    """
    return len(telefono) == 9 and telefono.isdigit()

def validarFechaNacimiento(fecha_nacimiento):
    # Validar que la fecha de nacimiento sea anterior al 2020
    """
    Comprueba que una fecha sea valida
    :param fecha_nacimiento: Recibe la fecha
    :return: True o False en funcion de si es valida o no
    """
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        return 2020 > fecha_nac.year > 1950
    except ValueError:
        return False

def validarDescripcion(descripcion):
    # Validar que la descripción tenga más de 4 caracteres
    """
    Comprueba que la descripcion tenga al menos 5 caracteres
    :param descripcion: EL nombre a validar
    :return: Si se cumple o no
    """
    return len(descripcion) > 5


def fallo(fallos, mensaje):
    """
    Metodo que permite gestionar los intentos en las acciones del usuario
    Muestra los errores actuales y los incrementa en 1
    :param fallos: Los fallos en ese momento
    :param mensaje: El mensaje que se quiere mostrar junto al numero de fallos
    :return: Devuelve los errores incrementados en 1
    """
    print(f"\t\t{mensaje} \n\t\tIntentos: {fallos + 1} de 5")
    return fallos + 1

def confirmacion(mensaje, tipo):
    """
    Metodo que permite la gestion de confirmaciones
    :param mensaje: La pregunta que se le hace al usuario
    :param tipo: Cadena para personalizar uno de los mensajes
    :return: True o False dependiendo de la eleccion del usuario
    """
    finConfirmacion = False
    fallos = 0
    while not finConfirmacion and fallos < 5:
        eleccion = input(f"{mensaje} [S/N]: ").lower()
        if eleccion == "s":
            finConfirmacion = True
            if tipo is not None:
                print(f"{tipo} realizada.")
            return True
        elif eleccion == "n":
            finConfirmacion = True
            if tipo is not None:
                print(f"{tipo} cancelada.")
            return False
        else:
            fallos = fallo(fallos, "Entrada no valida.")



def comprobarVacio (tabla):
    '''
    Metodo para comprobar si una tabla esta vacia
    :param tabla: Nombre de la tabla que se desea comprobar
    :return: Devuelve True o False en funcion de si la tabla esta vacia o no
    '''
    con, cur = gbd.conexion()

    try:
        cur.execute(f"select * from {tabla}")
        resultadoConsulta = cur.fetchone()

        if resultadoConsulta is None:
            print(f"La tabla {tabla} esta vacia")
            return False
        else:
            return True

    except Exception as comprobarTabla:
        print("Error al comprobar tabla en la BBDD", comprobarTabla)

    finally:
        gbd.confirmarEjecucionCerrarCursor(con, cur)
