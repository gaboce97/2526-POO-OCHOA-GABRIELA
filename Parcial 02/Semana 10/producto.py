"""
Módulo: producto.py
Descripción: Define la clase Producto que representa un producto en el inventario.
Autor: Sistema de Gestión de Inventarios
"""


class Producto:
    """
    Clase que representa un producto en el inventario.

    Atributos:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        cantidad (int): Cantidad disponible del producto
        precio (float): Precio unitario del producto
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.

        Args:
            id_producto (int): ID único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad inicial del producto
            precio (float): Precio unitario del producto
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # ============== GETTERS ==============

    def obtener_id(self):
        """Retorna el ID del producto."""
        return self._id

    def obtener_nombre(self):
        """Retorna el nombre del producto."""
        return self._nombre

    def obtener_cantidad(self):
        """Retorna la cantidad disponible del producto."""
        return self._cantidad

    def obtener_precio(self):
        """Retorna el precio unitario del producto."""
        return self._precio

    # ============== SETTERS ==============

    def establecer_nombre(self, nombre):
        """Establece un nuevo nombre para el producto."""
        if nombre.strip():
            self._nombre = nombre
        else:
            print(" Error: El nombre no puede estar vacío.")

    def establecer_cantidad(self, cantidad):
        """
        Establece una nueva cantidad del producto.

        Args:
            cantidad (int): Nueva cantidad (debe ser >= 0)
        """
        if cantidad >= 0:
            self._cantidad = cantidad
        else:
            print("Error: La cantidad no puede ser negativa.")

    def establecer_precio(self, precio):
        """
        Establece un nuevo precio del producto.

        Args:
            precio (float): Nuevo precio (debe ser >= 0)
        """
        if precio >= 0:
            self._precio = precio
        else:
            print("Error: El precio no puede ser negativo.")

    # ============== MÉTODOS ADICIONALES ==============

    def __str__(self):
        """Retorna una representación legible del producto."""
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"

    def mostrar_detalles(self):
        """Muestra los detalles completos del producto de forma formateada."""
        print(f"\n{'=' * 60}")
        print(f"ID del Producto: {self._id}")
        print(f"Nombre: {self._nombre}")
        print(f"Cantidad en Stock: {self._cantidad} unidades")
        print(f"Precio Unitario: ${self._precio:.2f}")
        print(f"Valor Total en Inventario: ${self._cantidad * self._precio:.2f}")
        print(f"{'=' * 60}\n")