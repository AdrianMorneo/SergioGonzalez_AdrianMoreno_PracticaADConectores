import GestionBBDD as gbd
import Utiles as ut
def nuevoCurso():

    """
    Permite crear nuevos cursos pidiendo al usuario los parametros adecuados
    si falla 3 veces en un parametro no crea el curso.
    El usuario puede elegir introducir otro curso despues de haber metido correctamente un curso
    :param: No recibe nada
    :return: No devuelve nada
    """
    finAlta = False
    while not finAlta:
        finAlta = True
        finEntradaAlta = False
        fallos = 0

        while not finEntradaAlta and fallos < 3:
            nombre = input("Nombre: ").strip().upper()
            if ut.validarNombre(nombre):
                print("\t\tNombre Valido\n")
                finEntradaAlta = True
            else:
                fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")

        finEntradaAlta = False
        if fallos < 3:
            fallos = 0
            while not finEntradaAlta and fallos < 3:
                descripcion = input("Descripcion: ").strip().upper()
                if ut.validarDireccion(descripcion):
                    print("\t\tDescripcion Valida\n")
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "La descripcion debe de contener mínimo 4 carácteres.")

        if fallos < 3:
            if ut.confirmacion("Dar de alta al curso?", "Alta"):
                gbd.nuevoCursoInsertBBDD(nombre, descripcion)
                if ut.confirmacion("Desea realizar otra Alta?", None):
                    finAlta = False

        else:
            print("\nAlta Cancelada.")

def buscarCurso():
    finEntradaAlta = False
    fallos = 0
    if ut.comprobarVacio("cursos"):
        while not finEntradaAlta and fallos < 3:
            nombre = input("Nombre: ").strip().upper()
            if ut.validarNombre(nombre):
                finEntradaAlta = True
                if gbd.buscarCursoBBDD(nombre):
                    return nombre
                else:
                    return ""
            else:
                fallos = ut.fallo(fallos, "El nombre debe contener al menos 2 caracteres.")
