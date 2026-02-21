"""
Módulo: inventario_modificado.py
Descripción: Define la clase Inventario que gestiona la colección de productos.
             Incluye almacenamiento persistente en archivo de texto y manejo de excepciones.
Autor: Sistema de Gestión de Inventarios
"""

from producto import Producto

# Nombre del archivo donde se guardará el inventario
ARCHIVO_INVENTARIO = "inventario.txt"


class Inventario:
    """
    Clase que gestiona el inventario de productos de la tienda.

    Atributos:
        _productos (list): Lista de objetos Producto almacenados en el inventario
        _archivo (str): Ruta del archivo de texto donde se persisten los datos
    """

    def __init__(self, archivo=ARCHIVO_INVENTARIO):
        """
        Constructor de la clase Inventario.
        Inicializa la lista de productos y carga los datos desde el archivo.

        Args:
            archivo (str): Ruta del archivo de inventario (por defecto 'inventario.txt')
        """
        self._productos = []
        self._archivo = archivo
        # Al iniciar, se cargan automáticamente los productos guardados
        self._cargar_desde_archivo()

    # ============== MÉTODOS DE ARCHIVO ==============

    def _cargar_desde_archivo(self):
        """
        Carga los productos desde el archivo de inventario al iniciar el programa.
        Si el archivo no existe, lo crea vacío.
        Maneja excepciones de archivo no encontrado y permisos.
        """
        try:
            with open(self._archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            # Si el archivo está vacío, no hay nada que cargar
            if not lineas:
                print("📂 Archivo de inventario encontrado pero vacío. Empezando sin productos.")
                return

            productos_cargados = 0
            for numero_linea, linea in enumerate(lineas, start=1):
                linea = linea.strip()
                # Ignorar líneas vacías o comentarios
                if not linea or linea.startswith("#"):
                    continue
                try:
                    # Formato esperado: id,nombre,cantidad,precio
                    partes = linea.split(",")
                    if len(partes) != 4:
                        print(f"⚠️  Línea {numero_linea} ignorada (formato incorrecto): '{linea}'")
                        continue

                    id_producto = int(partes[0].strip())
                    nombre = partes[1].strip()
                    cantidad = int(partes[2].strip())
                    precio = float(partes[3].strip())

                    # Agregar producto directamente sin guardar (evitar escritura al cargar)
                    nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
                    self._productos.append(nuevo_producto)
                    productos_cargados += 1

                except ValueError:
                    # Línea con datos inválidos o corruptos
                    print(f"⚠️  Línea {numero_linea} ignorada (datos corruptos): '{linea}'")

            print(f"✅ Inventario cargado desde '{self._archivo}': {productos_cargados} producto(s) recuperado(s).")

        except FileNotFoundError:
            # El archivo no existe aún, se crea uno nuevo vacío
            print(f"📄 Archivo '{self._archivo}' no encontrado. Se creará uno nuevo.")
            self._crear_archivo_vacio()

        except PermissionError:
            # No se tienen permisos para leer el archivo
            print(f"🔒 Error de permisos: No se puede leer '{self._archivo}'. "
                  f"El inventario funcionará solo en memoria.")

        except OSError as e:
            # Cualquier otro error relacionado con el sistema de archivos
            print(f"❌ Error al abrir el archivo '{self._archivo}': {e}. "
                  f"El inventario funcionará solo en memoria.")

    def _crear_archivo_vacio(self):
        """
        Crea el archivo de inventario vacío con un encabezado explicativo.
        Maneja excepciones si no se puede crear el archivo.
        """
        try:
            with open(self._archivo, "w", encoding="utf-8") as f:
                f.write("# Archivo de inventario - Formato: id,nombre,cantidad,precio\n")
            print(f"✅ Archivo '{self._archivo}' creado exitosamente.")

        except PermissionError:
            print(f"🔒 Error de permisos: No se puede crear '{self._archivo}'. "
                  f"Los cambios no se guardarán en disco.")

        except OSError as e:
            print(f"❌ Error al crear el archivo '{self._archivo}': {e}.")

    def _guardar_en_archivo(self):
        """
        Guarda todos los productos actuales en el archivo de inventario.
        Sobrescribe el archivo con el estado actual del inventario.
        Maneja excepciones de permisos y otros errores de escritura.

        Returns:
            bool: True si se guardó correctamente, False si hubo algún error
        """
        try:
            with open(self._archivo, "w", encoding="utf-8") as f:
                # Escribir encabezado
                f.write("# Archivo de inventario - Formato: id,nombre,cantidad,precio\n")
                # Escribir cada producto en una línea
                for producto in self._productos:
                    linea = (f"{producto.obtener_id()},"
                             f"{producto.obtener_nombre()},"
                             f"{producto.obtener_cantidad()},"
                             f"{producto.obtener_precio()}\n")
                    f.write(linea)
            return True

        except PermissionError:
            print(f"🔒 Error de permisos: No se pudo guardar en '{self._archivo}'. "
                  f"El cambio se aplicó en memoria pero no en disco.")
            return False

        except OSError as e:
            print(f"❌ Error al escribir en '{self._archivo}': {e}. "
                  f"El cambio se aplicó en memoria pero no en disco.")
            return False

    # ============== MÉTODOS PRINCIPALES ==============

    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        """
        Añade un nuevo producto al inventario y lo guarda en el archivo.

        Args:
            id_producto (int): ID único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad inicial
            precio (float): Precio unitario

        Returns:
            bool: True si se agregó exitosamente, False si hubo algún error
        """
        # Verificar que el ID sea único
        if self._id_existe(id_producto):
            print(f"❌ Error: Ya existe un producto con ID {id_producto}.")
            return False

        # Validar que los datos sean válidos
        if not nombre.strip():
            print("❌ Error: El nombre del producto no puede estar vacío.")
            return False

        if cantidad < 0 or precio < 0:
            print("❌ Error: La cantidad y el precio no pueden ser negativos.")
            return False

        # Crear y añadir el producto en memoria
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self._productos.append(nuevo_producto)

        # Guardar el inventario actualizado en el archivo
        if self._guardar_en_archivo():
            print(f"✅ Producto '{nombre}' agregado y guardado en '{self._archivo}' exitosamente.")
        else:
            print(f"⚠️  Producto '{nombre}' agregado en memoria, pero no se pudo guardar en archivo.")

        return True

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario y actualiza el archivo.

        Args:
            id_producto (int): ID del producto a eliminar

        Returns:
            bool: True si se eliminó exitosamente, False si no se encontró
        """
        for i, producto in enumerate(self._productos):
            if producto.obtener_id() == id_producto:
                nombre = producto.obtener_nombre()
                self._productos.pop(i)

                # Guardar el inventario actualizado en el archivo
                if self._guardar_en_archivo():
                    print(f"✅ Producto '{nombre}' (ID: {id_producto}) eliminado y archivo actualizado.")
                else:
                    print(f"⚠️  Producto '{nombre}' eliminado en memoria, pero no se pudo actualizar el archivo.")

                return True

        print(f"❌ Error: No se encontró producto con ID {id_producto}.")
        return False

    def actualizar_cantidad(self, id_producto, nueva_cantidad):
        """
        Actualiza la cantidad de un producto y guarda los cambios en el archivo.

        Args:
            id_producto (int): ID del producto
            nueva_cantidad (int): Nueva cantidad (debe ser >= 0)

        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        if nueva_cantidad < 0:
            print("❌ Error: La cantidad no puede ser negativa.")
            return False

        producto = self._buscar_producto_por_id(id_producto)
        if producto:
            cantidad_anterior = producto.obtener_cantidad()
            producto.establecer_cantidad(nueva_cantidad)

            # Guardar el inventario actualizado en el archivo
            if self._guardar_en_archivo():
                print(f"✅ Cantidad actualizada: {cantidad_anterior} → {nueva_cantidad} unidades. Archivo guardado.")
            else:
                print(f"⚠️  Cantidad actualizada en memoria ({cantidad_anterior} → {nueva_cantidad}), "
                      f"pero no se pudo guardar en archivo.")
            return True

        print(f"❌ Error: No se encontró producto con ID {id_producto}.")
        return False

    def actualizar_precio(self, id_producto, nuevo_precio):
        """
        Actualiza el precio de un producto y guarda los cambios en el archivo.

        Args:
            id_producto (int): ID del producto
            nuevo_precio (float): Nuevo precio (debe ser >= 0)

        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        if nuevo_precio < 0:
            print("❌ Error: El precio no puede ser negativo.")
            return False

        producto = self._buscar_producto_por_id(id_producto)
        if producto:
            precio_anterior = producto.obtener_precio()
            producto.establecer_precio(nuevo_precio)

            # Guardar el inventario actualizado en el archivo
            if self._guardar_en_archivo():
                print(f"✅ Precio actualizado: ${precio_anterior:.2f} → ${nuevo_precio:.2f}. Archivo guardado.")
            else:
                print(f"⚠️  Precio actualizado en memoria (${precio_anterior:.2f} → ${nuevo_precio:.2f}), "
                      f"pero no se pudo guardar en archivo.")
            return True

        print(f"❌ Error: No se encontró producto con ID {id_producto}.")
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
        return [
            producto for producto in self._productos
            if nombre_busqueda in producto.obtener_nombre().lower()
        ]

    def mostrar_todos_productos(self):
        """ Muestra todos los productos en el inventario de forma formateada."""
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
        """Verifica si ya existe un producto con el ID especificado."""
        return any(producto.obtener_id() == id_producto for producto in self._productos)

    def _buscar_producto_por_id(self, id_producto):
        """Busca un producto por su ID. Retorna el producto o None si no existe."""
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




