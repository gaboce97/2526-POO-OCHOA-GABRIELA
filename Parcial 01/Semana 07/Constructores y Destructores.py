

#Ejemplo 1: Uso de constructores y destructores en una clase Mascota

print("Ejemplo 1 - Constructores y Destructores en una clase Mascota")

class Mascota:
    # Clase para representar una mascota con datos básicos

    def __init__(self, nombre, tipo):
        # Constructor: inicializa nombre y tipo de mascota
        self.nombre = nombre
        self.tipo = tipo
        self.edad = 0
        print(f"✓ Mascota '{self.nombre}' ({self.tipo}) ha nacido")

    def hacer_sonido(self):
        # La mascota hace un sonido según su tipo
        sonidos = {"perro": "Guau!", "gato": "Miau!", "pajaro": "Pio pio!"}
        print(f"  {self.nombre} dice: {sonidos.get(self.tipo, '...')}")

    def __del__(self):
        # Destructor: se ejecuta cuando la mascota es eliminada
        print(f"✓ Mascota '{self.nombre}' ha sido eliminada")

# Crear instancias de Mascota
mi_perro = Mascota("Rex", "perro")
mi_gato = Mascota("Misu", "gato")
mi_pajaro = Mascota("Tweety", "pajaro")
mi_perro.hacer_sonido()
mi_gato.hacer_sonido()
mi_pajaro.hacer_sonido()
# Eliminar las instancias para ver el destructor en acción
del mi_perro
del mi_gato
del mi_pajaro

print("------------------------------------------------------------------")

#Ejemplo 2: Uso de constructores y destructores en una clase Libro

print("Ejemplo 2 - Constructores y Destructores en una clase Libro")
class Libro:
    # Clase para representar un libro con título, autor y año de publicación

    def __init__(self, titulo, autor, anio):
        # Constructor: inicializa título, autor y año
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        print(f"✓ Libro '{self.titulo}' de {self.autor} ({self.anio}) ha sido creado")

    def mostrar_info(self):
        # Muestra la información del libro
        print(f"  Título: {self.titulo}, Autor: {self.autor}, Año: {self.anio}")

    def __del__(self):
        # Destructor: se ejecuta cuando el libro es eliminado
        print(f"✓ Libro '{self.titulo}' ha sido eliminado")

# Crear instancias de Libro
libro1 = Libro("1984", "George Orwell", 1949)
libro2 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 1967)
libro1.mostrar_info()
libro2.mostrar_info()
# Eliminar las instancias para ver el destructor en acción
del libro1
del libro2

print("------------------------------------------------------------------")

#Ejemplo 3: Uso de constructores y destructores en una clase Estudiante
print("Ejemplo 3 - Constructores y Destructores en una clase Estudiante")

class Estudiante:
    # Clase para gestionar información de estudiantes

    def __init__(self, nombre, matricula):
        # Constructor: inicializa nombre y matrícula
        self.nombre = nombre
        self.matricula = matricula
        self.calificaciones = []
        print(f"✓ Estudiante '{self.nombre}' (Matrícula: {self.matricula}) registrado")

    def agregar_calificacion(self, nota):
        # Agrega una calificación al estudiante
        self.calificaciones.append(nota)
        print(f"  Calificación agregada: {nota}")

    def __del__(self):
        # Destructor: limpia los datos del estudiante al ser eliminado
        promedio = sum(self.calificaciones) / len(self.calificaciones) if self.calificaciones else 0
        print(f"✓ Estudiante '{self.nombre}' eliminado (Promedio: {promedio:.2f})")


# Crear instancias de Estudiante
estudiante1 = Estudiante("Ana", "A001")
estudiante2 = Estudiante("Luis", "A002")
estudiante1.agregar_calificacion(85)
estudiante1.agregar_calificacion(90)
estudiante2.agregar_calificacion(78)
estudiante2.agregar_calificacion(88)
# Eliminar las instancias para ver el destructor en acción
del estudiante1
del estudiante2





