import GestionBBDD as GBD
import Utiles as ut
def nuevoProfesorPedirValores():
    def alta():
        """
        Permite crear nuevos profesores
        :param: No recibe nada
        :return: No devuelve nada
        """
        finAlta = False
        while not finAlta:
            finAlta = True
            finEntradaAlta = False
            fallos = 0


            while not finEntradaAlta and fallos < 3:
                dni = input("DNI: ").strip().upper()
                if ut.validarDNI(dni):
                    finEntradaAlta = True
                else:
                    fallos = ut.fallo(fallos, "El Dni debe tener 8 numeros y una letra")

            finEntradaAlta = False

            if fallos < 3:
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
                    direccion = input("Direccion: ").strip().upper()
                    if ut.validarDireccion(direccion):
                        print("\t\tDirección Valida\n")
                        finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "La dirección debe de contener mínimo 4 carácteres.")

            finEntradaAlta = False
            if fallos < 3:
                fallos = 0
                while not finEntradaAlta and fallos < 3:
                    telefono = input("Telefono: ").strip()
                    if ut.validarTelefono(telefono):
                        print("\t\tTelefono Valido\n")
                        finEntradaAlta = True
                    else:
                        fallos = ut.fallo(fallos, "Formato incorrecto, debe de tener 9 dígitos.")

            if fallos < 3:
                if ut.confirmacion("Dar de alta al profesor?", "Alta"):
                    GBD.nuevoProfesorInsertBBDD(dni,nombre,direccion,telefono)
                    print("Profesor dado de alta correcctamente")
                    if ut.confirmacion("Desea realizar otra Alta?", None):
                        finAlta = False

            else:
                print("\nAlta Cancelada.")


