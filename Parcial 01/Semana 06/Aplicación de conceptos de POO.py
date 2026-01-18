#tienda de productos de belleza usando POO
#USO DE HERENCIA, ENCAPSULAMIENTO Y POLIMORFISMO

# CLASE BASE
class Producto:
    def __init__(self, nombre, precio, categoria):
        self.__nombre = nombre  #atributo privado - encapsulamiento
        self.__precio = precio  #atributo privado - encapsulamiento
        self.__categoria = categoria   #atributo privado - encapsulamiento
#getters para acceder a los atributos privados
    def get_nombre(self):
        return self.__nombre

    def get_precio(self):
        return self.__precio

    def get_categoria(self):
        return self.__categoria

    def mostrar_info(self):  #metodo público - polimorfismo, puede ser sobrescrito
        return f"Producto: {self.__nombre}, Precio: ${self.__precio}, Categoría: {self.__categoria}"


# CLASES DERIVADAS - HERENCIA
class ProductoMaquillaje(Producto):
    def __init__(self, nombre, precio, categoria):
        super().__init__(nombre, precio, categoria)
        self.__descuento = 10

    def mostrar_info(self): #polimorfismo - se muestra solo la info de maquillaje
        precio_final = self.get_precio() - (self.get_precio() * self.__descuento / 100)
        return f" MAQUILLAJE | {super().mostrar_info()} | Precio Final: ${precio_final:.2f}"


class ProductoSkincare(Producto):
    def __init__(self, nombre, precio, categoria):
        super().__init__(nombre, precio, categoria)
        self.__caracteristica = "Vegano"

    def mostrar_info(self): #polimorfismo - se muestra solo la info de skincare
        return f" SKINCARE | {super().mostrar_info()} | {self.__caracteristica}"


# TIENDA
class Tienda:
    def __init__(self):
        self.productos = []

    def agregar(self, producto):
        self.productos.append(producto) #agregar producto a la lista

    def mostrar(self):
        print("\n" + "=" * 60)
        print("INVENTARIO")
        print("=" * 60)
        for p in self.productos:
            print(p.mostrar_info())
        print("=" * 60 + "\n")


# MAIN
if __name__ == "__main__":
    tienda = Tienda()

    # Crear productos
    p1 = ProductoMaquillaje("Labial MAC", 30, "Labios")
    p2 = ProductoMaquillaje("Mascara Sephora", 25, "Pestañas")
    p3 = ProductoSkincare("Crema Hidratante", 20, "Cuidado de la piel")
    # Agregar a tienda
    tienda.agregar(p1)
    tienda.agregar(p2)
    tienda.agregar(p3)

    # Mostrar inventario
    tienda.mostrar()
