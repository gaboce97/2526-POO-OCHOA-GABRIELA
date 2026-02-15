"""
Módulo: main.py
Descripción: Interfaz de usuario en consola para el Sistema de Gestión de Inventarios.
Autor: Sistema de Gestión de Inventarios
"""

from inventario import Inventario


def mostrar_menu_principal():
    """Muestra el menú principal de opciones."""
    print("\n" + "=" * 60)
    print("     SISTEMA DE GESTIÓN DE INVENTARIOS")
    print("=" * 60)
    print("1. ➕ Agregar nuevo producto")
    print("2. ❌ Eliminar producto")
    print("3. 📝 Actualizar producto (cantidad o precio)")
    print("4. 🔍 Buscar producto por nombre")
    print("5. 📊 Ver todos los productos")
    print("6. 📈 Ver estadísticas del inventario")
    print("7. ❌ Salir")
    print("=" * 60)


class InterfazInventario:
    """
    Clase que maneja la interfaz de usuario en consola para el inventario.
    Proporciona un menú interactivo para realizar todas las operaciones del inventario.
    """

    def __init__(self):
        """Constructor que inicializa el inventario y prepara la interfaz."""
        self.inventario = Inventario()
        self._cargar_datos_ejemplo()

    def _cargar_datos_ejemplo(self):
        """
        Carga algunos datos de ejemplo en el inventario para facilitar las pruebas.
        Comentar esta línea si se desea empezar con un inventario vacío.
        """
        print("\n Cargando datos de ejemplo...\n")
        self.inventario.agregar_producto(1, "Laptop Dell", 5, 899.99)
        self.inventario.agregar_producto(2, "Mouse Logitech", 15, 29.99)
        self.inventario.agregar_producto(3, "Teclado Mecánico", 8, 129.99)
        self.inventario.agregar_producto(4, "Monitor LG 24\"", 3, 249.99)
        self.inventario.agregar_producto(5, "Cable HDMI", 20, 9.99)

    def opcion_agregar_producto(self):
        """Maneja la opción de agregar un nuevo producto."""
        print("\n--- AGREGAR NUEVO PRODUCTO ---")
        try:
            id_producto = int(input("Ingrese el ID del producto: "))
            nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad inicial: "))
            precio = float(input("Ingrese el precio unitario: $"))

            self.inventario.agregar_producto(id_producto, nombre, cantidad, precio)
        except ValueError:
            print(" Error: Ingrese datos válidos (ID y cantidad deben ser números).")

    def opcion_eliminar_producto(self):
        """Maneja la opción de eliminar un producto."""
        print("\n--- ELIMINAR PRODUCTO ---")
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            self.inventario.eliminar_producto(id_producto)
        except ValueError:
            print(" Error: El ID debe ser un número.")

    def opcion_actualizar_producto(self):
        """Maneja la opción de actualizar un producto."""
        print("\n--- ACTUALIZAR PRODUCTO ---")
        try:
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))

            print("\n¿Qué desea actualizar?")
            print("1. Cantidad")
            print("2. Precio")
            print("3. Ambos")

            opcion = input("Seleccione una opción (1-3): ").strip()

            if opcion == "1":
                nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                self.inventario.actualizar_cantidad(id_producto, nueva_cantidad)
            elif opcion == "2":
                nuevo_precio = float(input("Ingrese el nuevo precio: $"))
                self.inventario.actualizar_precio(id_producto, nuevo_precio)
            elif opcion == "3":
                nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                nuevo_precio = float(input("Ingrese el nuevo precio: $"))
                self.inventario.actualizar_cantidad(id_producto, nueva_cantidad)
                self.inventario.actualizar_precio(id_producto, nuevo_precio)
            else:
                print(" Opción no válida.")
        except ValueError:
            print(" Error: Ingrese datos válidos.")

    def opcion_buscar_producto(self):
        """Maneja la opción de buscar productos por nombre."""
        print("\n--- BUSCAR PRODUCTO ---")
        nombre_busqueda = input("Ingrese parte del nombre del producto a buscar: ").strip()

        if not nombre_busqueda:
            print(" Error: Debe ingresar un término de búsqueda.")
            return

        productos = self.inventario.buscar_por_nombre(nombre_busqueda)

        if not productos:
            print(f"\n  No se encontraron productos con '{nombre_busqueda}'.")
        else:
            print(f"\n Se encontraron {len(productos)} producto(s):\n")
            print("=" * 80)
            print(f"{'ID':<5} {'Nombre':<30} {'Cantidad':<12} {'Precio':<15}")
            print("=" * 80)

            for producto in productos:
                print(f"{producto.obtener_id():<5} "
                      f"{producto.obtener_nombre():<30} "
                      f"{producto.obtener_cantidad():<12} "
                      f"${producto.obtener_precio():<14.2f}")

            print("=" * 80 + "\n")

            # Opción para ver detalles de un producto específico
            try:
                ver_detalles = input("¿Desea ver detalles de algún producto? (s/n): ").lower()
                if ver_detalles == 's':
                    id_detalles = int(input("Ingrese el ID del producto: "))
                    for producto in productos:
                        if producto.obtener_id() == id_detalles:
                            producto.mostrar_detalles()
                            break
            except ValueError:
                print(" Error: Ingrese un ID válido.")

    def opcion_ver_todos(self):
        """Maneja la opción de ver todos los productos."""
        print("\n--- TODOS LOS PRODUCTOS EN EL INVENTARIO ---")
        self.inventario.mostrar_todos_productos()

    def opcion_estadisticas(self):
        """Muestra estadísticas generales del inventario."""
        print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
        print("=" * 60)
        cantidad_productos = self.inventario.obtener_cantidad_productos()
        valor_total = self.inventario.obtener_valor_total_inventario()

        print(f"Total de productos diferentes: {cantidad_productos}")
        print(f"Valor total del inventario: ${valor_total:.2f}")

        if cantidad_productos > 0:
            print(f"Valor promedio por producto: ${valor_total / cantidad_productos:.2f}")

        print("=" * 60 + "\n")

    def ejecutar(self):
        """
        Ejecuta el loop principal de la aplicación.
        Muestra el menú y procesa las opciones del usuario.
        """
        print("\n¡Bienvenido al Sistema de Gestión de Inventarios!\n")

        while True:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción (1-7): ").strip()

            if opcion == "1":
                self.opcion_agregar_producto()
            elif opcion == "2":
                self.opcion_eliminar_producto()
            elif opcion == "3":
                self.opcion_actualizar_producto()
            elif opcion == "4":
                self.opcion_buscar_producto()
            elif opcion == "5":
                self.opcion_ver_todos()
            elif opcion == "6":
                self.opcion_estadisticas()
            elif opcion == "7":
                print("\n¡Gracias por usar el Sistema de Gestión de Inventarios!")
                print(" ¡Hasta luego!\n")
                break
            else:
                print(" Opción no válida. Por favor, seleccione una opción entre 1 y 7.")

            input("\nPresione Enter para continuar...")


def main():
    """Función principal que inicia la aplicación."""
    aplicacion = InterfazInventario()
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()