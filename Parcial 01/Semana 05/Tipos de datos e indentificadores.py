"""
PROGRAMA: Gestor de Registro de Estudiantes
DESCRIPCIÓN: Este programa gestiona un registro básico de estudiantes.
Permite ver y agregar nuevos estudiantes. Incluye algunos estudiantes
de ejemplo al iniciar.
"""


class Estudiante:
    """
    Clase que representa un estudiante.
    Almacena: nombre, edad, matrícula y calificación.
    """

    def __init__(self, nombre, edad, matricula, calificacion):
        """
        Constructor de la clase Estudiante.

        Parámetros:
            nombre (string): Nombre del estudiante.
            edad (integer): Edad del estudiante.
            matricula (string): Número de matrícula.
            calificacion (float): Calificación del estudiante.
        """
        self.nombre = nombre
        self.edad = edad
        self.matricula = matricula
        self.calificacion = calificacion

    def mostrar_info(self):
        """
        Muestra la información del estudiante.
        """
        print(f"  {self.nombre} - Edad: {self.edad} - Mat: {self.matricula} - Cal: {self.calificacion:.1f}")


class GestorEstudiantes:
    """
    Clase que gestiona el registro de estudiantes.
    """

    def __init__(self):
        """
        Constructor que inicializa la lista con estudiantes de ejemplo.

        Atributos:
            estudiantes (list): Lista de estudiantes.
        """
        self.estudiantes = [
            Estudiante("Juan García", 20, "001", 8.5),
            Estudiante("María López", 21, "002", 9.0),
            Estudiante("Carlos Rodríguez", 19, "003", 7.5),
            Estudiante("Ana Martínez", 20, "004", 8.8),
            Estudiante("Pedro Sánchez", 22, "005", 7.2)
        ]

    def mostrar_todos(self):
        """
        Muestra todos los estudiantes registrados.
        """
        print("\n" + "=" * 55)
        print("              REGISTRO DE ESTUDIANTES")
        print("=" * 55)

        for index, estudiante in enumerate(self.estudiantes, 1):
            print(f"{index}. ", end="")
            estudiante.mostrar_info()

        print("=" * 55)

    def agregar_estudiante(self):
        """
        Solicita datos y agrega un nuevo estudiante al registro.
        """
        print("\n--- AGREGAR NUEVO ESTUDIANTE ---")

        try:
            # Solicitar nombre (string)
            nombre = input("Nombre: ").strip()

            # Solicitar edad (integer)
            edad = int(input("Edad: "))

            # Solicitar matrícula (string)
            matricula = input("Matrícula: ").strip()

            # Solicitar calificación (float)
            calificacion = float(input("Calificación: "))

            # Crear y agregar estudiante
            estudiante = Estudiante(nombre, edad, matricula, calificacion)
            self.estudiantes.append(estudiante)

            print(f"✅ Estudiante '{nombre}' agregado correctamente.")

        except ValueError:
            print("❌ Ingresa datos válidos.")

    def mostrar_menu(self):
        """
        Muestra el menú principal.
        """
        while True:
            print("\n" + "=" * 55)
            print("           GESTOR DE ESTUDIANTES")
            print("=" * 55)
            print("1. Ver todos los estudiantes")
            print("2. Agregar nuevo estudiante")
            print("3. Salir")
            print("=" * 55)

            opcion = input("Opción (1-3): ").strip()

            if opcion == "1":
                self.mostrar_todos()
            elif opcion == "2":
                self.agregar_estudiante()
            elif opcion == "3":
                print("\n¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida.")


# Punto de entrada del programa
if __name__ == "__main__":
    gestor = GestorEstudiantes()
    gestor.mostrar_menu()



"""
- Tipos de datos utilizados:
string: nombre, matrícula
integer: edad
float: calificación
list: almacena estudiantes

- Identificadores utilizados:
Clases: Estudiante, GestorEstudiantes
Métodos: __init__, mostrar_info, mostrar_todos, agregar_estudiante, mostrar_menu
Variables: nombre, edad, matricula, calificacion, estudiantes, index, opcion


"""