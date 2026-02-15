"""
Módulo: inventario.py
Descripción: Define la clase Inventario que gestiona la colección de productos.
Autor: Sistema de Gestión de Inventarios
"""

from producto import Producto


class Inventario:
    """
    Clase que gestiona el inventario de productos de la tienda.

    Atributos:
        productos (list): Lista de objetos Producto almacenados en el inventario
    """

    def __init__(self):
        """Constructor de la clase Inventario. Inicializa una lista vacía de productos."""
        self._productos = []

    # ============== MÉTODOS PRINCIPALES ==============

    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        """
        Añade un nuevo producto al inventario.

        Args:
            id_producto (int): ID único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad inicial
            precio (float): Precio unitario

        Returns:
            bool: True si se agregó exitosamente, False si el ID ya existe
        """
        # Verificar que el ID sea único
        if self._id_existe(id_producto):
            print(f"Error: Ya existe un producto con ID {id_producto}.")
            return False

        # Validar que los datos sean válidos
        if not nombre.strip():
            print("Error: El nombre del producto no puede estar vacío.")
            return False

        if cantidad < 0 or precio < 0:
            print("Error: La cantidad y el precio no pueden ser negativos.")
            return False

        # Crear y añadir el producto
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self._productos.append(nuevo_producto)
        print(f"Producto '{nombre}' agregado exitosamente.")
        return True

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.

        Args:
            id_producto (int): ID del producto a eliminar

        Returns:
            bool: True si se eliminó exitosamente, False si no se encontró
        """
        for i, producto in enumerate(self._productos):
            if producto.obtener_id() == id_producto:
                nombre = producto.obtener_nombre()
                self._productos.pop(i)
                print(f"Producto '{nombre}' (ID: {id_producto}) eliminado exitosamente.")
                return True

        print(f"Error: No se encontró producto con ID {id_producto}.")
        return False

    def actualizar_cantidad(self, id_producto, nueva_cantidad):
        """
        Actualiza la cantidad de un producto por su ID.

        Args:
            id_producto (int): ID del producto
            nueva_cantidad (int): Nueva cantidad (debe ser >= 0)

        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        if nueva_cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            return False

        producto = self._buscar_producto_por_id(id_producto)
        if producto:
            cantidad_anterior = producto.obtener_cantidad()
            producto.establecer_cantidad(nueva_cantidad)
            print(f"Cantidad actualizada: {cantidad_anterior} → {nueva_cantidad} unidades")
            return True

        print(f"Error: No se encontró producto con ID {id_producto}.")
        return False

    def actualizar_precio(self, id_producto, nuevo_precio):
        """
        Actualiza el precio de un producto por su ID.

        Args:
            id_producto (int): ID del producto
            nuevo_precio (float): Nuevo precio (debe ser >= 0)

        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        if nuevo_precio < 0:
            print(" Error: El precio no puede ser negativo.")
            return False

        producto = self._buscar_producto_por_id(id_producto)
        if producto:
            precio_anterior = producto.obtener_precio()
            producto.establecer_precio(nuevo_precio)
            print(f"Precio actualizado: ${precio_anterior:.2f} → ${nuevo_precio:.2f}")
            return True

        print(f"Error: No se encontró producto con ID {id_producto}.")
        return False

    def buscar_por_nombre(self, nombre_busqueda):
        """
        Busca productos cuyo nombre contenga la cadena de búsqueda (case-insensitive).

        Args:
            nombre_busqueda (str): Parte del nombre a buscar

        Returns:
            list: Lista de productos encontrados
        """
        nombre_busqueda = nombre_busqueda.lower()
        productos_encontrados = [
            producto for producto in self._productos
            if nombre_busqueda in producto.obtener_nombre().lower()
        ]

        return productos_encontrados

    def mostrar_todos_productos(self):
        """Muestra todos los productos en el inventario de forma formateada."""
        if not self._productos:
            print("\n  El inventario está vacío.\n")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Nombre':<25} {'Cantidad':<12} {'Precio':<15} {'Total':<15}")
        print("=" * 80)

        total_valor = 0
        for producto in self._productos:
            valor_producto = producto.obtener_cantidad() * producto.obtener_precio()
            total_valor += valor_producto

            print(f"{producto.obtener_id():<5} "
                  f"{producto.obtener_nombre():<25} "
                  f"{producto.obtener_cantidad():<12} "
                  f"${producto.obtener_precio():<14.2f} "
                  f"${valor_producto:<14.2f}")

        print("=" * 80)
        print(f"{'VALOR TOTAL DEL INVENTARIO:':<57} ${total_valor:.2f}")
        print("=" * 80 + "\n")

    # ============== MÉTODOS PRIVADOS (AUXILIARES) ==============

    def _id_existe(self, id_producto):
        """
        Verifica si ya existe un producto con el ID especificado.

        Args:
            id_producto (int): ID a verificar

        Returns:
            bool: True si el ID existe, False en caso contrario
        """
        return any(producto.obtener_id() == id_producto for producto in self._productos)

    def _buscar_producto_por_id(self, id_producto):
        """
        Busca un producto por su ID.

        Args:
            id_producto (int): ID del producto a buscar

        Returns:
            Producto: El producto encontrado, None si no existe
        """
        for producto in self._productos:
            if producto.obtener_id() == id_producto:
                return producto
        return None

    def obtener_cantidad_productos(self):
        """Retorna la cantidad total de productos diferentes en el inventario."""
        return len(self._productos)

    def obtener_valor_total_inventario(self):
        """Retorna el valor total de todos los productos en el inventario."""
        return sum(
            producto.obtener_cantidad() * producto.obtener_precio()
            for producto in self._productos
        )