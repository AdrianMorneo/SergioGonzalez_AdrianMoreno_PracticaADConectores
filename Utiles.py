
from datetime import datetime


def validarDNI(dni):
    # Validar DNI con 8 números y una letra al final
    return len(dni) == 9 and dni[:-1].isdigit() and dni[-1].isalpha()


def validarNombre(nombre):
    # Validar que el nombre tenga más de 2 caracteres
    return len(nombre) > 2

def validarDireccion(direccion):
    # Validar que la dirección tenga más de 4 caracteres
    return len(direccion) > 4

def validarTelefono(telefono):
    # Validar que el teléfono tenga 9 números
    return len(telefono) == 9 and telefono[:0].isdigit()

def validarFechaNacimiento(fecha_nacimiento):
    # Validar que la fecha de nacimiento sea anterior al 2020
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        return fecha_nac.year < 2020
    except ValueError:
        return False

def validarDescripcion(descripcion):
    # Validar que la descripción tenga más de 5 caracteres
    return len(descripcion) > 5


def fallo(fallos, mensaje):
    """
    Metodo que permite gestionar los intentos en las acciones del usuario
    Muestra los errores actuales y los incrementa en 1
    :param fallos: Los fallos en ese momento
    :param mensaje: El mensaje que se quiere mostrar junto al numero de fallos
    :return: Devuelve los errores incrementados en 1
    """
    print(f"\t\t{mensaje} \n\t\tIntentos: {fallos + 1} de 3")
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
    while not finConfirmacion and fallos < 3:
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


