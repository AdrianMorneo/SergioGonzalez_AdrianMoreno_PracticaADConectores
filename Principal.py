
while True:
    # Menú principal
    print("\nBienvenido al Centro de Estudios de Adrian y Sergio")
    print("--------------------------------------------------")
    print("1. Profesores")
    print("2. Alumnos")
    print("3. Cursos")
    print("0. Salir")
    opcion_principal = input("\nSeleccione una opción (1, 2, 3, 0): ")

    if opcion_principal == '1':
        # Submenú de Profesores
        while True:
            print("\nSubMenu Profesores:")
            print("--------------------")
            print("1. Nuevo profesor")
            print("2. Eliminar profesor")
            print("3. Modificar profesor")
            print("4. Buscar profesor")
            print("5. Mostrar todos los profesores")
            print("9. Volver al menú principal")
            print("0. Salir")
            opcion_profesores = input("\nSeleccione una opción (1-5, 9, 0): ")

            if opcion_profesores == '1':
                print("\n-- Has seleccionado: Nuevo profesor --")
                # Lógica para nuevo profesor
                pass
            elif opcion_profesores == '2':
                print("\n-- Has seleccionado: Eliminar profesor --")
                # Lógica para eliminar profesor
                pass
            elif opcion_profesores == '3':
                print("\n-- Has seleccionado: Modificar profesor --")
                # Lógica para modificar profesor
                pass
            elif opcion_profesores == '4':
                print("\n-- Has seleccionado: Buscar profesor --")
                # Lógica para buscar profesor
                pass
            elif opcion_profesores == '5':
                print("\n-- Has seleccionado: Mostrar todos los profesores --")
                # Lógica para mostrar todos los profesores
                pass
            elif opcion_profesores == '9':
                break
            elif opcion_profesores == '0':
                exit()

    elif opcion_principal == '2':
        # Submenú de Alumnos
        while True:
            print("\nSubMenu Alumnos:")
            print("----------------")
            print("1. Nuevo alumno")
            print("2. Eliminar alumno")
            print("3. Modificar alumno")
            print("4. Buscar alumno")
            print("5. Mostrar todos los alumnos")
            print("9. Volver al menú principal")
            print("0. Salir")
            opcion_alumnos = input("\nSeleccione una opción (1-5, 9, 0): ")

            if opcion_alumnos == '1':
                print("\n-- Has seleccionado: Nuevo alumno --")
                # Lógica para nuevo alumno
                pass
            elif opcion_alumnos == '2':
                print("\n-- Has seleccionado: Eliminar alumno --")
                # Lógica para eliminar alumno
                pass
            elif opcion_alumnos == '3':
                print("\n-- Has seleccionado: Modificar alumno --")
                # Lógica para modificar alumno
                pass
            elif opcion_alumnos == '4':
                print("\n-- Has seleccionado: Buscar alumno --")
                # Lógica para buscar alumno
                pass
            elif opcion_alumnos == '5':
                print("\n-- Has seleccionado: Mostrar todos los alumnos --")
                # Lógica para mostrar todos los alumnos
                pass
            elif opcion_alumnos == '9':
                break
            elif opcion_alumnos == '0':
                exit()

    elif opcion_principal == '3':
        # Submenú de Cursos
        while True:
            print("\nSubMenu Cursos:")
            print("---------------")
            print("1. Nuevo curso")
            print("2. Eliminar curso")
            print("3. Modificar curso")
            print("4. Buscar curso")
            print("5. Mostrar todos los cursos")
            print("9. Volver al menú principal")
            print("0. Salir")
            opcion_cursos = input("\nSeleccione una opción (1-5, 9, 0): ")

            if opcion_cursos == '1':
                print("\n-- Has seleccionado: Nuevo curso --")
                # Lógica para nuevo curso
                pass
            elif opcion_cursos == '2':
                print("\n-- Has seleccionado: Eliminar curso --")
                # Lógica para eliminar curso
                pass
            elif opcion_cursos == '3':
                print("\n-- Has seleccionado: Modificar curso --")
                # Lógica para modificar curso
                pass
            elif opcion_cursos == '4':
                print("\n-- Has seleccionado: Buscar curso --")
                # Lógica para buscar curso
                pass
            elif opcion_cursos == '5':
                print("\n-- Has seleccionado: Mostrar todos los cursos --")
                # Lógica para mostrar todos los cursos
                pass
            elif opcion_cursos == '9':
                break
            elif opcion_cursos == '0':
                exit()

    elif opcion_principal == '0':
        exit()
    else:
        print("\nOpción no válida. Inténtelo de nuevo.")