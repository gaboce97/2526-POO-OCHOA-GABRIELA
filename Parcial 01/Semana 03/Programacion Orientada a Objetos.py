#Programación Orientada a Objetos (POO)

#Determinar promedio semanal del clima de una ciudad

#Definición de la clase ClimaSemanal

class ClimaSemanal:
    def __init__(self):
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"] # Lista de días de la semana
        self.temperaturas = []  # Lista para almacenar las temperaturas diarias
        self.suma_temperaturas = 0  # Variable para almacenar la suma de las temperaturas
        self.promedio_semanal = 0  # Variable para almacenar el promedio semanal

    def capturar_temperaturas(self):
        for dia in self.dias:
            temp = float(input(f"Ingrese la temperatura del {dia}: "))  # Captura la temperatura diaria
            self.temperaturas.append(temp)  # Agrega la temperatura a la lista

    def calcular_promedio(self):
        for temp in self.temperaturas:
            self.suma_temperaturas += temp  # Suma cada temperatura a la variable suma_temperaturas
        self.promedio_semanal = self.suma_temperaturas / len(self.temperaturas)  # Calcula el promedio

    def mostrar_promedio(self):
        print(f"El promedio semanal de temperaturas es: {self.promedio_semanal:.2f} grados centígrados.")  # Muestra el promedio con dos decimales

#Uso de la clase ClimaSemanal
clima = ClimaSemanal()  # Crea una instancia de la clase ClimaSemanal
clima.capturar_temperaturas()  # Llama al metodo para capturar temperaturas
clima.calcular_promedio()      # Llama al metodo para calcular el promedio
clima.mostrar_promedio()       # Llama al metodo para mostrar el promedio


#-----------------------------------------------------------------------------

#la abstracción se usa al definir la clase ClimaSemanal que encapsula todos los datos y métodos relacionados
# con el cálculo del promedio semanal de temperaturas. Los detalles internos de cómo se capturan, calculan y
# muestran las temperaturas están ocultos dentro de la clase, proporcionando una interfaz clara para interactuar con ella.

#El encapsulamiento se observa en el uso de atributos y métodos dentro de la clase ClimaSemanal.
# Los atributos como dias, temperaturas, suma_temperaturas y promedio_semanal están encapsulados dentro de la clase,
# y solo se accede a ellos a través de los métodos definidos (capturar_temperaturas, calcular_promedio, mostrar_promedio).
# Esto protege los datos internos y asegura que solo se modifiquen de manera controlada a través de los métodos de la clase.

#La herencia no se aplica en este ejemplo específico, ya que no hay clases derivadas que extiendan la funcionalidad de ClimaSemanal.

#El polimorfismo tampoco se ilustra en este ejemplo, ya que no hay múltiples clases con métodos que compartan el mismo nombre pero se comporten de manera diferente.