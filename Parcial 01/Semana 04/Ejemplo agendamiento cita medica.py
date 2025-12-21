#Ejemplo de un sistema de citas medicas

# Clase para representar un paciente
class Paciente:
    def __init__(self, nombre, edad, cedula):
        self.nombre = nombre            # Nombre del paciente
        self.edad = edad                # Edad del paciente
        self.cedula = cedula            # Cédula del paciente

# str es un metodo especial que define la representacion en cadena del objeto, osea como se ve cuando se imprime
    def __str__(self):
        return f"Paciente: {self.nombre}, Edad: {self.edad}, Cédula: {self.cedula}"

# Clase padre para todas las citas médicas
class Cita:
    def __init__(self, paciente, fecha, hora):
        self.paciente = paciente        # Objeto Paciente
        self.fecha = fecha              # Fecha de la cita
        self.hora = hora                # Hora de la cita

# Clase hija para Cardiología
class CitaCardiologia(Cita):
    def __init__(self, paciente, fecha, hora):
        super().__init__(paciente, fecha, hora)
        self.doctor = "Dr. Carlos Martínez"
        self.especialidad = "Cardiología"

    def __str__(self):
        return (f"{self.paciente.nombre} cita en {self.especialidad} -"
                f" {self.doctor} |  {self.fecha} {self.hora}")

# Clase hija para Gastroenterología
class CitaGastroenterologia(Cita):
    def __init__(self, paciente, fecha, hora):
        super().__init__(paciente, fecha, hora)
        self.doctor = "Dra. Isabel Vivanco"
        self.especialidad = "Gastroenterología"

    def __str__(self):
        return (f"{self.paciente.nombre} cita en {self.especialidad} -"
                f" {self.doctor} |  {self.fecha} {self.hora}")

# Clase hija para Pediatría
class CitaPediatria(Cita):
    def __init__(self, paciente, fecha, hora):
        super().__init__(paciente, fecha, hora)
        self.doctor = "Dr. Roberth Espinoza"
        self.especialidad = "Pediatría"

    def __str__(self):
        return (f"{self.paciente.nombre} cita en {self.especialidad} -"
                f" {self.doctor} |  {self.fecha} {self.hora}")

# - Ejemplo de uso del sistema de citas médicas -

print(" SISTEMA DE CITAS MÉDICAS \n")

# Crear pacientes
paciente1 = Paciente("Carlos Medina", 45, "1234567")
paciente2 = Paciente("María Gonzales", 38, "2345678")
paciente3 = Paciente("Gabriela Ochoa", 8, "3456789")
paciente4 = Paciente("Ana Celi", 32, "4567890")

# Agendar citas
cita1 = CitaCardiologia(paciente1, "15/01/2025", "10:00")
cita2 = CitaGastroenterologia(paciente2, "16/01/2025", "11:30")
cita3 = CitaPediatria(paciente3, "17/01/2025", "09:00")
cita4 = CitaCardiologia(paciente4, "17/01/2025", "14:00")

# Mostrar citas agendadas
print(" - CITAS AGENDADAS -\n")
print(cita1)
print(cita2)
print(cita3)
print(cita4)