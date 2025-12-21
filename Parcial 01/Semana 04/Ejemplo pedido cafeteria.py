#Mostrar el pedido de un cliente en una cafetería

# Clase base para todos los productos
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    # Metodo que retorna la información del producto
    def mostrar_info(self):
        return f"{self.nombre} - ${self.precio}"

# Clase Bebida que hereda de Producto
class Bebida(Producto):
    def __init__(self, nombre, precio, tamaño):
        # super() llama al constructor de la clase padre (Producto)
        super().__init__(nombre, precio)
        self.tamaño = tamaño

# Clase Comida que hereda de Producto
class Comida(Producto):
    def __init__(self, nombre, precio, tipo):
        # super() llama al constructor de la clase padre (Producto)
        super().__init__(nombre, precio)
        self.tipo = tipo

# Clase que representa cada artículo en el pedido
class ItemPedido:
    def __init__(self, producto, cantidad):
        self.productos = producto  # Almacena el producto
        self.cantidad = cantidad    # Cantidad del producto

    # Calcula el subtotal multiplicando precio por cantidad
    def subtotal(self):
        return self.productos.precio * self.cantidad

    # Retorna una descripción formateada del item
    def descripcion(self):
        return f"{self.cantidad} x {self.productos.mostrar_info()} = ${self.subtotal()}"

# Clase que representa el pedido completo del cliente
class Pedido:
    def __init__(self):
        self.items = []  # Lista para almacenar los items del pedido

    # Metodo para agregar un producto al pedido
    def agregar_item(self, producto, cantidad):
        # Crea un nuevo ItemPedido
        item = ItemPedido(producto, cantidad)
        # Lo agrega a la lista de items
        self.items.append(item)
        print(f" Agregado: {item.descripcion()}")

    # Calcula el total del pedido sumando todos los subtotales
    def total(self):
        return sum(item.subtotal() for item in self.items)

    # Muestra el detalle completo del pedido
    def mostrar_pedido(self):
        print("\n - Detalle del Pedido ")
        for item in self.items:
            print(item.descripcion())
        print(f"Total a pagar: ${self.total()}")


# Clase que administra el menú de la cafetería
class Menu:
    def __init__(self):
        self.bebidas = []  # Lista de bebidas disponibles
        self.comidas = []  # Lista de comidas disponibles

    # Metodo para agregar una bebida al menú
    def agregar_bebida(self, bebida):
        self.bebidas.append(bebida)

    # Metodo para agregar una comida al menú
    def agregar_comida(self, comida):
        self.comidas.append(comida)

    # Muestra todas las bebidas y comidas del menú
    def mostrar(self):
        print(" - Menu de Bebidas ")
        for bebida in self.bebidas:
            print(f"- {bebida.mostrar_info()} ({bebida.tamaño})")
        print("\n- Menu de Comidas ")
        for comida in self.comidas:
            print(f"- {comida.mostrar_info()} ({comida.tipo})")

#  EJEMPLO DE USO
# Crear una instancia del menú
menu = Menu()

# Agregar bebidas al menú
menu.agregar_bebida(Bebida("Café", 2.5, "Mediano"))
menu.agregar_bebida(Bebida("Té", 2.0, "Grande"))
menu.agregar_bebida(Bebida("Jugo de Naranja", 3.0, "Pequeño"))
menu.agregar_bebida(Bebida("Capuchino", 4.0, "Mediano"))
menu.agregar_bebida(Bebida("Agua Mineral", 1.5, "Grande"))

# Agregar comidas al menú
menu.agregar_comida(Comida("Humita", 1.0, "Salado"))
menu.agregar_comida(Comida("Ensalada", 4.5, "Salado"))
menu.agregar_comida(Comida("Pastel de Chocolate", 3.5, "Dulce"))
menu.agregar_comida(Comida("Brownie", 2.5, "Dulce"))
menu.agregar_comida(Comida("Sándwich", 5.0, "Salado"))

# Mostrar el menú disponible
menu.mostrar()

# Crear un nuevo pedido
print("\n--- Realizando un pedido ---")
pedido = Pedido()

# Agregar items al pedido
# [0] es el índice (posición) del producto en la lista
pedido.agregar_item(menu.bebidas[3], 2)  # 2 Capuchinos
pedido.agregar_item(menu.comidas[0], 1)  # 1 Humita
pedido.agregar_item(menu.comidas[2], 1)  # 1 Pastel de Chocolate

# Mostrar el pedido completo con el total
pedido.mostrar_pedido()