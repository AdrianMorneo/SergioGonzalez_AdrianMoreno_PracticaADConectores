import GestionBBDD as gbd
import Utiles as ut
def nuevoProfesor():

    """
    Permite crear nuevos profesores pidiendo al usuario los parametros adecuados
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


        while not finEntradaAlta and fallos < 5:
            dni = input("DNI: ").strip().upper()
            if ut.validarDNI(dni):
                print("\t\tDNI Valido\n")
                finEntradaAlta = True
            else:
                fallos = ut.fallo(fallos, "El Dni debe tener 8 numeros y una letra")

        finEntradaAlta = False

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
                telefono = input("Telefono: ").strip()
                if ut.validarTelefono(telefono):
                    print("\t\tTelefono Valido\n")
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "Formato incorrecto, debe de tener 9 dígitos.")

        if fallos < 5:
            if ut.confirmacion("Dar de alta al profesor?", "Alta"):
                gbd.nuevoProfesorInsertBBDD(dni, nombre, direccion, telefono)
                if ut.confirmacion("Desea realizar otra Alta?", None):
                    finAlta = False

        else:
            print("\nAlta Cancelada.")

def buscarProfesor():
    finEntradaAlta = False
    fallos = 0
    if ut.comprobarVacio("profesores"):
        while not finEntradaAlta and fallos < 5:
            dni = input("DNI: ").strip().upper()
            if ut.validarDNI(dni):
                finEntradaAlta = True
                if gbd.buscarProfesorBBDD(dni) != 0:
                    return dni
                else:
                    return ""
            else:
                fallos = ut.fallo(fallos, "El Dni debe tener 8 numeros y una letra")
