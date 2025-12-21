# ejemplo de una galería de arte con diferentes aristas y obras de arte.

# Clase para representar una obra de arte
class Obra:
    def __init__(self, titulo, artista, precio):
        self.titulo = titulo        # Título de la obra
        self.artista = artista      # Nombre del artista
        self.precio = precio        # Precio de la obra

#metodo str para representar la obra como cadena
    def __str__(self):
        return f"'{self.titulo}' - {self.artista} - ${self.precio}"

# Clase para representar una galería de arte
class Galeria:
    def __init__(self, nombre):
        self.nombre = nombre        # Nombre de la galería
        self.obras = []             # Lista de obras

#metodo para agregar una obra a la galería
#append agrega la obra al final de la lista

    def agregar_obra(self, obra):
        self.obras.append(obra)

#metodo para mostrar todas las obras en la galería

    def mostrar(self):
        print(f"\n GALERÍA {self.nombre.upper()} \n")
        for obra in self.obras:
            print(f"  • {obra}")

# - EJEMPLO DE USO -

# Crear galería
galeria = Galeria(": Arte Moderno en Santa Rosa")

# Crear obras
obra1 = Obra("Guernica", "Pablo Picasso", 50000)
obra2 = Obra("Noche Estrellada", "Vincent van Gogh", 75000)
obra3 = Obra("Persistencia de la Memoria", "Salvador Dalí", 60000)
obra4 = Obra("Grito", "Edvard Munch", 45000)
obra5 = Obra("Gato Durmiendo", "Anónimo", 500)
obra6 = Obra("Mona Lisa", "Leonardo da Vinci", 850000)

# Agregar obras a la galería
galeria.agregar_obra(obra1)
galeria.agregar_obra(obra2)
galeria.agregar_obra(obra3)
galeria.agregar_obra(obra4)
galeria.agregar_obra(obra5)
galeria.agregar_obra(obra6)

# Mostrar galería
galeria.mostrar()