import GestionBBDD as gbd
import Utiles as ut
'''
número de expediente, nombre, apellidos, teléfono, dirección y
fecha de nacimiento.
'''
def nuevoAlumno():

    """
    Permite crear nuevos alumnos pidiendo al usuario los parametros adecuados
    si falla 3 veces en un parametro no crea el profesor.
    El usuario puede elegir introducir otro profesor despues de haber metido corretamente un profesor
    :param: No recibe nada
    :return: No devuelve nada
    """
    finAlta = False
    while not finAlta:
        finAlta = True
        finEntradaAlta = False
        fallos = 0

        if fallos < 5:
            fallos = 0
            while not finEntradaAlta and fallos < 5:
                nombre = input("Nombre: ").strip().upper()
                if ut.validarNombre(nombre):
                    print("\t\tNombre Valido\n")
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")

        finEntradaAlta = False
        if fallos < 5:
            fallos = 0
            while not finEntradaAlta and fallos < 5:
                apellidos = input("Apellidos: ").strip().upper()
                if ut.validarNombre(apellidos):
                    if not alumnoRepe(nombre,apellidos):
                        print("\t\tApellidos Validos\n")
                        finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, f"Ya existe un alumno con el nombre {nombre} y el apellido {apellidos}")
                else:
                    fallos = ut.fallo(fallos, "Los apellidos deben contener al menos 2 caracteres.")
        finEntradaAlta = False
        if fallos < 5:
            fallos = 0
            while not finEntradaAlta and fallos < 5:
                telefono = input("Telefono: ").strip()
                if ut.validarTelefono(telefono):
                    if not tlfRepe(telefono):
                        print("\t\tTelefono Valido\n")
                        finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "El telefono introducido ya existe en otro alumno.")
                else:
                    fallos = ut.fallo(fallos, "Formato incorrecto, debe de tener 9 dígitos.")

        finEntradaAlta = False
        if fallos < 5:
            fallos = 0
            while not finEntradaAlta and fallos < 5:
                direccion = input("Direccion: ").strip().upper()
                if ut.validarDireccion(direccion):
                    print("\t\tDirección Valida\n")
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

        finEntradaAlta = False
        if fallos < 5:
            fallos = 0
            while not finEntradaAlta and fallos < 5:
                fechaNacimiento = input("Fecha de nacimiento: ").strip()
                if ut.validarFechaNacimiento(fechaNacimiento):
                    print("\t\tFecha de nacimiento Valida\n")
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "Fecha no valida ,deben ser numeros con el siguiente formato: yyyy-mm-dd")

        if fallos < 5:

            gbd.nuevoAlumnoInsertBBDD(nombre, apellidos, telefono, direccion ,fechaNacimiento)
            if ut.confirmacion("Desea realizar otra Alta?", None):
                finAlta = False

        else:
            print("\nAlta Cancelada.")

def buscarAlumno():
    finEntradaAlta = False
    fallos = 0
    if ut.comprobarVacio("alumnos"):
        while not finEntradaAlta and fallos < 5:
            nombre = input("Nombre del alumno : ").strip().upper()
            if ut.validarNombre(nombre):
                finEntradaAlta = True
            else:
                fallos = ut.fallo(fallos, "El nombre debe tener al menos dos caracteres ")
        finEntradaAlta = False
        while not finEntradaAlta and fallos < 5:
            apellidos = input("Apellidos del alumno : ").strip().upper()
            if ut.validarNombre(apellidos):
                finEntradaAlta = True
            else:
                fallos = ut.fallo(fallos, "Los apellidos debe tener al menos 2 caracteres ")
        if apellidos is not None and nombre is not None:
            if gbd.buscarAlumnoBBDD(nombre , apellidos ) != 0:
                return nombre, apellidos
            else:
                return ""

def alumnoRepe(nombre , apellidos):

    con, cur = gbd.conexion()
    cur.execute(f"SELECT * FROM alumnos WHERE Nombre = '{nombre}' AND Apellidos = '{apellidos}'")
    repetido = cur.fetchone()

    if repetido is not None:
        return True
    else:
        return False

def tlfRepe(telefono):

    con, cur = gbd.conexion()
    cur.execute(f"SELECT * FROM alumnos WHERE Telefono = '{telefono}' ")
    repetido = cur.fetchone()
    if repetido is not None:
        return True
    else:
        return False