"""
Sistema Avanzado de Gestión de Inventario de un minimarket
==========================================
Descripción: Sistema de gestión de inventario utilizando POO, colecciones y
             almacenamiento persistente en archivos JSON.

Colecciones utilizadas:
- Diccionario (dict): almacén principal del inventario {id: Producto}
- Conjunto (set): registro de IDs usados para evitar duplicados rápidamente
- Lista (list): resultados de búsquedas temporales
- Tupla (tuple): representación inmutable de un snapshot de producto
"""

import json
import os

# ─────────────────────────────────────────────
# CLASE PRODUCTO
# ─────────────────────────────────────────────
class Producto:
    """Representa un producto dentro del inventario."""

    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        self.__id_producto = id_producto   # Atributo privado – ID único
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # ── Getters ──────────────────────────────
    def get_id(self) -> str:
        return self.__id_producto

    def get_nombre(self) -> str:
        return self.__nombre

    def get_cantidad(self) -> int:
        return self.__cantidad

    def get_precio(self) -> float:
        return self.__precio

    # ── Setters ──────────────────────────────
    def set_nombre(self, nombre: str):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre.strip()

    def set_cantidad(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    # ── Utilidades ───────────────────────────
    def a_diccionario(self) -> dict:
        """Serializa el producto a un diccionario (para guardar en JSON)."""
        return {
            "id": self.__id_producto,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }

    def a_tupla(self) -> tuple:
        """Devuelve una tupla inmutable con los datos del producto (snapshot)."""
        return self.__id_producto, self.__nombre, self.__cantidad, self.__precio

    def __str__(self) -> str:
        return (f"  ID: {self.__id_producto:<10} | Nombre: {self.__nombre:<20} | "
                f"Cantidad: {self.__cantidad:<6} | Precio: ${self.__precio:.2f}")


# ─────────────────────────────────────────────
# CLASE INVENTARIO
# ─────────────────────────────────────────────
class Inventario:
    """
    Gestiona la colección de productos.

    Colecciones internas:
    - self.__productos (dict):  clave = ID, valor = objeto Producto
    - self.__ids_usados (set):  conjunto de IDs ya registrados (búsqueda O(1))
    """

    ARCHIVO_DATOS = "inventario.json"

    def __init__(self):
        self.__productos: dict[str, Producto] = {}   # Diccionario principal
        self.__ids_usados: set[str] = set()           # Conjunto de IDs

        # Cargar datos persistidos si existen
        self.cargar_desde_archivo()

    # ── Añadir producto ───────────────────────
    def agregar_producto(self, id_producto: str, nombre: str,
                         cantidad: int, precio: float):
        """Añade un nuevo producto al inventario."""
        if id_producto in self.__ids_usados:
            print(f"\n  Ya existe un producto con el ID '{id_producto}'.")
            return

        producto = Producto(id_producto, nombre, cantidad, precio)
        self.__productos[id_producto] = producto   # Inserción en diccionario
        self.__ids_usados.add(id_producto)          # Registro en conjunto
        self.guardar_en_archivo()
        print(f"\n✔  Producto '{nombre}' agregado correctamente.")

    # ── Eliminar producto ─────────────────────
    def eliminar_producto(self, id_producto: str):
        """Elimina un producto del inventario por su ID."""
        if id_producto not in self.__ids_usados:
            print(f"\n No se encontró ningún producto con ID '{id_producto}'.")
            return

        nombre = self.__productos[id_producto].get_nombre()
        del self.__productos[id_producto]
        self.__ids_usados.discard(id_producto)
        self.guardar_en_archivo()
        print(f"\n✔  Producto '{nombre}' (ID: {id_producto}) eliminado.")

    # ── Actualizar producto ───────────────────
    def actualizar_producto(self, id_producto: str,
                            nueva_cantidad: int = None,
                            nuevo_precio: float = None):
        """Actualiza la cantidad y/o el precio de un producto."""
        if id_producto not in self.__ids_usados:
            print(f"\n No se encontró ningún producto con ID '{id_producto}'.")
            return

        producto = self.__productos[id_producto]
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        self.guardar_en_archivo()
        print(f"\n✔  Producto '{producto.get_nombre()}' actualizado correctamente.")

    # ── Buscar por nombre ─────────────────────
    def buscar_por_nombre(self, termino: str) -> list:
        """
        Busca productos cuyo nombre contenga el término (sin distinción de
        mayúsculas/minúsculas). Retorna una lista de Producto.
        """
        termino = termino.lower().strip()
        # Comprensión de lista – crea una lista temporal con resultados
        resultados: list[Producto] = [
            p for p in self.__productos.values()
            if termino in p.get_nombre().lower()
        ]
        return resultados

    # ── Mostrar todos los productos ───────────
    def mostrar_todos(self):
        """Imprime todos los productos del inventario."""
        if not self.__productos:
            print("\n  (El inventario está vacío)")
            return

        print("\n" + "═" * 75)
        print(f"  {'INVENTARIO COMPLETO':^71}")
        print("═" * 75)
        for producto in self.__productos.values():
            print(producto)
        print("═" * 75)
        print(f"  Total de productos distintos: {len(self.__productos)}")

    # ── Resumen de categorías únicas ──────────
    def categorias_nombres(self) -> set:
        """
        Devuelve un conjunto con los nombres únicos de los primeros 'tokens'
        (palabras iniciales) de cada producto.  Ejemplo de uso de set.
        """
        return {p.get_nombre().split()[0] for p in self.__productos.values()}

    # ── Guardar en archivo ────────────────────
    def guardar_en_archivo(self):
        """
        Serializa el diccionario de productos a JSON y lo escribe en disco.
        Cada Producto se convierte a dict mediante su metodo a_diccionario() para asegurar compatibilidad con JSON.
        """
        datos = [p.a_diccionario() for p in self.__productos.values()]
        with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

    # ── Cargar desde archivo ──────────────────
    def cargar_desde_archivo(self):
        """
        Deserializa el inventario desde el archivo JSON, reconstruyendo los
        objetos Producto y repoblando el diccionario y el conjunto de IDs.
        """
        if not os.path.exists(self.ARCHIVO_DATOS):
            return  # Primera ejecución – no hay archivo todavía

        with open(self.ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            try:
                datos: list[dict] = json.load(archivo)
            except json.JSONDecodeError:
                print("⚠  El archivo de datos está corrupto. Iniciando inventario vacío.")
                return

        for d in datos:
            producto = Producto(d["id"], d["nombre"], d["cantidad"], d["precio"])
            self.__productos[d["id"]] = producto
            self.__ids_usados.add(d["id"])

        print(f"✔  Inventario cargado: {len(self.__productos)} productos encontrados.")


# ─────────────────────────────────────────────
# FUNCIONES DE INTERFAZ DE USUARIO
# ─────────────────────────────────────────────

def leer_entero(mensaje: str, minimo: int = 0) -> int:
    """Lee un entero validado desde la consola."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"  Ingresa un valor ≥ {minimo}.")
            else:
                return valor
        except ValueError:
            print("  Valor inválido. Intenta de nuevo.")


def leer_flotante(mensaje: str, minimo: float = 0.0) -> float:
    """Lee un flotante validado desde la consola."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                print(f"  Ingresa un valor ≥ {minimo}.")
            else:
                return valor
        except ValueError:
            print("  Valor inválido. Intenta de nuevo.")


def menu_agregar(inventario: Inventario):
    print("\n── AGREGAR PRODUCTO ──")
    id_p    = input("  ID del producto   : ").strip()
    nombre  = input("  Nombre            : ").strip()
    cantidad = leer_entero("  Cantidad          : ", 0)
    precio   = leer_flotante("  Precio ($)        : ", 0.0)
    inventario.agregar_producto(id_p, nombre, cantidad, precio)


def menu_eliminar(inventario: Inventario):
    print("\n── ELIMINAR PRODUCTO ──")
    id_p = input("  ID del producto a eliminar: ").strip()
    inventario.eliminar_producto(id_p)


def menu_actualizar(inventario: Inventario):
    print("\n── ACTUALIZAR PRODUCTO ──")
    id_p = input("  ID del producto a actualizar: ").strip()
    print("  (Presiona Enter para no modificar un campo)")

    nueva_cantidad = None
    nueva_cantidad_str = input("  Nueva cantidad    : ").strip()
    if nueva_cantidad_str:
        nueva_cantidad = int(nueva_cantidad_str)

    nuevo_precio = None
    nuevo_precio_str = input("  Nuevo precio ($)  : ").strip()
    if nuevo_precio_str:
        nuevo_precio = float(nuevo_precio_str)

    inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio)


def menu_buscar(inventario: Inventario):
    print("\n── BUSCAR PRODUCTO ──")
    termino = input("  Nombre o parte del nombre: ").strip()
    resultados = inventario.buscar_por_nombre(termino)

    if not resultados:
        print(f"\n  No se encontraron productos con '{termino}'.")
    else:
        print(f"\n  {len(resultados)} resultado(s) para '{termino}':")
        print("─" * 75)
        for p in resultados:
            print(p)
        print("─" * 75)


def mostrar_menu():
    print("\n" + "═" * 45)
    print("   SISTEMA DE GESTIÓN DE INVENTARIO")
    print("═" * 45)
    print("  1. Agregar producto")
    print("  2. Eliminar producto")
    print("  3. Actualizar producto")
    print("  4. Buscar producto por nombre")
    print("  5. Mostrar todos los productos")
    print("  6. Salir")
    print("═" * 45)


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────
def main():
    inventario = Inventario()

    opciones = {
        "1": menu_agregar,
        "2": menu_eliminar,
        "3": menu_actualizar,
        "4": menu_buscar,
        "5": lambda inv: inv.mostrar_todos(),
    }

    while True:
        mostrar_menu()
        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "6":
            print("\n  ¡Hasta luego! Los datos han sido guardados.\n")
            break
        elif opcion in opciones:
            try:
                opciones[opcion](inventario)
            except ValueError as e:
                print(f"\n⚠  Error de validación: {e}")
        else:
            print("\n  Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()