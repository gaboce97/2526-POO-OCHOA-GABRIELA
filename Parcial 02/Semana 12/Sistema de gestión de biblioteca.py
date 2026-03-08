"""
  SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL
Implementa la gestión de libros, usuarios y préstamos
usando listas, tuplas, diccionarios y conjuntos de forma
estratégica según las propiedades de cada dato.
"""

from datetime import date


# ──────────────────────────────────────────────────────
# CLASE: Libro
# ──────────────────────────────────────────────────────
class Libro:
    """
    Representa un libro de la biblioteca.

    Se usa una TUPLA para (autor, título) porque son datos
    inmutables: una vez publicado, el libro no cambia de autor
    ni de título. Esto también permite usar la tupla como
    clave en estructuras hash si fuera necesario.
    """

    def __init__(self, isbn: str, titulo: str, autor: str,
                 categoria: str, copias: int = 1):
        # ISBN como identificador único (clave en el diccionario)
        self.isbn = isbn.strip().upper()

        # Tupla inmutable: (autor, título)
        self._info_inmutable: tuple[str, str] = (autor.strip(), titulo.strip())

        self.categoria = categoria.strip().lower()

        # Copias totales y disponibles para gestionar préstamos simultáneos
        self.copias_totales = copias
        self.copias_disponibles = copias

    # ── Propiedades de solo lectura derivadas de la tupla ──
    @property
    def autor(self) -> str:
        return self._info_inmutable[0]

    @property
    def titulo(self) -> str:
        return self._info_inmutable[1]

    @property
    def disponible(self) -> bool:
        return self.copias_disponibles > 0

    def __repr__(self) -> str:
        estado = f"{self.copias_disponibles}/{self.copias_totales} copias"
        return (f"Libro(isbn={self.isbn!r}, título={self.titulo!r}, "
                f"autor={self.autor!r}, categoría={self.categoria!r}, "
                f"{estado})")


# ──────────────────────────────────────────────────────
# CLASE: Usuario
# ──────────────────────────────────────────────────────
class Usuario:
    """
    Representa a un usuario registrado en la biblioteca.

    Se usa una LISTA para los libros prestados porque:
    - El orden de préstamo puede importar.
    - Los elementos cambian con frecuencia (préstamos y devoluciones).
    - Permite duplicados si el usuario tomara dos copias del mismo libro.
    """

    def __init__(self, nombre: str, usuario_id: str):
        self.nombre = nombre.strip()
        # ID normalizado a mayúsculas para evitar duplicados por capitalización
        self.usuario_id = usuario_id.strip().upper()

        # Lista mutable de ISBNs prestados actualmente al usuario
        self.libros_prestados: list[str] = []

        # Historial completo: lista de tuplas (isbn, fecha_prestamo, fecha_devolucion|None)
        self.historial: list[tuple[str, date, date | None]] = []

    def __repr__(self) -> str:
        return (f"Usuario(id={self.usuario_id!r}, nombre={self.nombre!r}, "
                f"prestados={len(self.libros_prestados)})")


# ──────────────────────────────────────────────────────
# CLASE: Biblioteca
# ──────────────────────────────────────────────────────
class Biblioteca:
    """
    Gestiona el catálogo, los usuarios y los préstamos.

    Estructuras de datos empleadas:
    - DICCIONARIO  _catalogo      → ISBN (str) : Libro   (búsqueda O(1))
    - DICCIONARIO  _usuarios      → user_id    : Usuario (búsqueda O(1))
    - CONJUNTO     _ids_usuarios  → IDs únicos registrados      (O(1) pertenencia)
    """

    def __init__(self, nombre: str):
        self.nombre = nombre

        # Diccionario principal de libros: ISBN → Libro
        self._catalogo: dict[str, Libro] = {}

        # Diccionario de usuarios: user_id → Usuario
        self._usuarios: dict[str, Usuario] = {}

        # Conjunto de IDs únicos; garantiza unicidad sin recorrer la lista
        self._ids_usuarios: set[str] = set()

    # ══════════════════════════════════════════════════
    # GESTIÓN DE LIBROS
    # ══════════════════════════════════════════════════

    def agregar_libro(self, libro: Libro) -> None:
        """Añade un libro al catálogo o incrementa sus copias si ya existe."""
        if libro.isbn in self._catalogo:
            # Si el ISBN ya está, sumamos las copias nuevas
            existente = self._catalogo[libro.isbn]
            existente.copias_totales += libro.copias_totales
            existente.copias_disponibles += libro.copias_disponibles
            print(f"  [+] Copias actualizadas → {existente}")
        else:
            self._catalogo[libro.isbn] = libro
            print(f"  [+] Libro añadido → {libro}")

    def quitar_libro(self, isbn: str) -> None:
        """Elimina un libro del catálogo (solo si no tiene copias prestadas)."""
        isbn = isbn.strip().upper()
        if isbn not in self._catalogo:
            print(f"  [!] ISBN {isbn!r} no encontrado en el catálogo.")
            return

        libro = self._catalogo[isbn]
        prestadas = libro.copias_totales - libro.copias_disponibles
        if prestadas > 0:
            print(f"  [!] No se puede quitar '{libro.titulo}': "
                  f"{prestadas} copia(s) aún prestada(s).")
            return

        del self._catalogo[isbn]
        print(f"  [-] Libro eliminado: ISBN {isbn!r}")

    # ══════════════════════════════════════════════════
    # GESTIÓN DE USUARIOS
    # ══════════════════════════════════════════════════

    def registrar_usuario(self, usuario: Usuario) -> None:
        """Registra un nuevo usuario. Rechaza IDs duplicados."""
        if usuario.usuario_id in self._ids_usuarios:
            print(f"  [!] ID '{usuario.usuario_id}' ya registrado.")
            return

        # Añade al diccionario Y al conjunto en la misma operación
        self._usuarios[usuario.usuario_id] = usuario
        self._ids_usuarios.add(usuario.usuario_id)
        print(f"  [+] Usuario registrado → {usuario}")

    def dar_baja_usuario(self, usuario_id: str) -> None:
        """Da de baja a un usuario (solo si no tiene libros pendientes)."""
        usuario_id = usuario_id.strip().upper()
        if usuario_id not in self._ids_usuarios:
            print(f"  [!] Usuario ID '{usuario_id}' no encontrado.")
            return

        usuario = self._usuarios[usuario_id]
        if usuario.libros_prestados:
            print(f"  [!] No se puede dar de baja a '{usuario.nombre}': "
                  f"tiene {len(usuario.libros_prestados)} libro(s) sin devolver.")
            return

        del self._usuarios[usuario_id]
        self._ids_usuarios.discard(usuario_id)   # discard no lanza error si no existe
        print(f"  [-] Usuario dado de baja: '{usuario.nombre}' (ID: {usuario_id})")

    # ══════════════════════════════════════════════════
    # PRÉSTAMOS Y DEVOLUCIONES
    # ══════════════════════════════════════════════════

    def prestar_libro(self, usuario_id: str, isbn: str) -> None:
        """
        Presta un libro a un usuario.
        - Verifica existencia de usuario e ISBN.
        - Verifica disponibilidad de copias.
        - Registra en la lista de préstamos del usuario y en su historial.
        """
        usuario_id = usuario_id.strip().upper()
        isbn = isbn.strip().upper()

        # Validar usuario
        if usuario_id not in self._ids_usuarios:
            print(f"  [!] Usuario '{usuario_id}' no registrado.")
            return

        # Validar libro
        if isbn not in self._catalogo:
            print(f"  [!] ISBN '{isbn}' no existe en el catálogo.")
            return

        libro = self._catalogo[isbn]
        usuario = self._usuarios[usuario_id]

        # Verificar disponibilidad
        if not libro.disponible:
            print(f"  [!] '{libro.titulo}' no tiene copias disponibles.")
            return

        # Realizar el préstamo
        libro.copias_disponibles -= 1
        usuario.libros_prestados.append(isbn)
        usuario.historial.append((isbn, date.today(), None))

        print(f"  [✓] Préstamo realizado: '{libro.titulo}' → '{usuario.nombre}' "
              f"({libro.copias_disponibles} cop. disponibles)")

    def devolver_libro(self, usuario_id: str, isbn: str) -> None:
        """
        Procesa la devolución de un libro.
        - Actualiza la lista de préstamos del usuario (list.remove).
        - Actualiza el historial con la fecha de devolución.
        - Incrementa las copias disponibles del libro.
        """
        usuario_id = usuario_id.strip().upper()
        isbn = isbn.strip().upper()

        if usuario_id not in self._ids_usuarios:
            print(f"  [!] Usuario '{usuario_id}' no registrado.")
            return

        usuario = self._usuarios[usuario_id]

        if isbn not in usuario.libros_prestados:
            print(f"  [!] El usuario '{usuario.nombre}' no tiene prestado el ISBN '{isbn}'.")
            return

        libro = self._catalogo[isbn]
        # Eliminar la primera ocurrencia (en caso de múltiples copias del mismo libro)
        usuario.libros_prestados.remove(isbn)
        libro.copias_disponibles += 1

        # Actualizar historial: buscar el registro abierto (fecha_dev = None)
        for i, (h_isbn, f_prest, f_dev) in enumerate(usuario.historial):
            if h_isbn == isbn and f_dev is None:
                usuario.historial[i] = (h_isbn, f_prest, date.today())
                break

        print(f"  [✓] Devolución: '{libro.titulo}' ← '{usuario.nombre}' "
              f"({libro.copias_disponibles} cop. disponibles)")

    # ══════════════════════════════════════════════════
    # BÚSQUEDAS
    # ══════════════════════════════════════════════════

    def buscar_por_titulo(self, texto: str) -> list[Libro]:
        """Búsqueda parcial e insensible a mayúsculas por título."""
        texto = texto.lower()
        return [l for l in self._catalogo.values() if texto in l.titulo.lower()]

    def buscar_por_autor(self, texto: str) -> list[Libro]:
        """Búsqueda parcial e insensible a mayúsculas por autor."""
        texto = texto.lower()
        return [l for l in self._catalogo.values() if texto in l.autor.lower()]

    def buscar_por_categoria(self, categoria: str) -> list[Libro]:
        """Búsqueda exacta (insensible a mayúsculas) por categoría."""
        categoria = categoria.lower()
        return [l for l in self._catalogo.values() if l.categoria == categoria]

    # ══════════════════════════════════════════════════
    # LISTADOS
    # ══════════════════════════════════════════════════

    def listar_prestamos_usuario(self, usuario_id: str) -> None:
        """Muestra todos los libros actualmente prestados a un usuario."""
        usuario_id = usuario_id.strip().upper()
        if usuario_id not in self._ids_usuarios:
            print(f"  [!] Usuario '{usuario_id}' no encontrado.")
            return

        usuario = self._usuarios[usuario_id]
        print(f"\n  📚 Libros prestados a '{usuario.nombre}' (ID: {usuario_id}):")
        if not usuario.libros_prestados:
            print("      (ninguno)")
            return

        for isbn in usuario.libros_prestados:
            libro = self._catalogo.get(isbn)
            titulo = libro.titulo if libro else "(libro eliminado)"
            print(f"      • ISBN {isbn} — {titulo}")

    def listar_historial_usuario(self, usuario_id: str) -> None:
        """Muestra el historial completo de préstamos de un usuario."""
        usuario_id = usuario_id.strip().upper()
        if usuario_id not in self._ids_usuarios:
            print(f"  [!] Usuario '{usuario_id}' no encontrado.")
            return

        usuario = self._usuarios[usuario_id]
        print(f"\n  🗂  Historial de '{usuario.nombre}':")
        if not usuario.historial:
            print("      (vacío)")
            return

        for isbn, f_prest, f_dev in usuario.historial:
            libro = self._catalogo.get(isbn)
            titulo = libro.titulo if libro else "(libro eliminado)"
            devolucion = str(f_dev) if f_dev else "en préstamo"
            print(f"      • {titulo} | prestado: {f_prest} | devuelto: {devolucion}")

    def mostrar_catalogo(self) -> None:
        """Imprime el catálogo completo."""
        print(f"\n  📖 Catálogo de '{self.nombre}' ({len(self._catalogo)} libro(s)):")
        if not self._catalogo:
            print("      (vacío)")
            return
        for libro in self._catalogo.values():
            estado = "✅ disponible" if libro.disponible else "❌ no disponible"
            print(f"      [{estado}] {libro.titulo} — {libro.autor} "
                  f"(ISBN: {libro.isbn}, cat: {libro.categoria})")


# ══════════════════════════════════════════════════════
# BLOQUE DE PRUEBAS
# ══════════════════════════════════════════════════════
def separador(titulo: str) -> None:
    print(f"\n{'═'*55}")
    print(f"  {titulo}")
    print(f"{'═'*55}")


if __name__ == "__main__":

    # ── 1. Crear la biblioteca ──────────────────────────
    separador("1. CREACIÓN DE LA BIBLIOTECA")
    bib = Biblioteca("Biblioteca Digital Cervantes")
    print(f"  Biblioteca '{bib.nombre}' creada.")

    # ── 2. Añadir libros ────────────────────────────────
    separador("2. AÑADIR LIBROS AL CATÁLOGO")
    libros = [
        Libro("978-0-06-112008-4", "Matar a un ruiseñor",      "Harper Lee",          "ficción",   2),
        Libro("978-0-7432-7356-5", "1984",                     "George Orwell",       "distopía",  3),
        Libro("978-0-14-028329-7", "El gran Gatsby",           "F. Scott Fitzgerald", "ficción",   1),
        Libro("978-0-06-093546-9", "Para matar un ruiseñor",   "Harper Lee",          "ficción",   1),
        Libro("978-3-16-148410-0", "Cien años de soledad",     "Gabriel García Márquez","realismo mágico", 2),
        Libro("978-0-525-55360-5", "El alquimista",            "Paulo Coelho",        "aventura",  4),
        Libro("978-0-316-76948-0", "El guardián entre el centeno","J.D. Salinger",    "ficción",   2),
    ]
    for l in libros:
        bib.agregar_libro(l)

    # Intentar añadir un libro con ISBN duplicado (suma copias)
    print()
    bib.agregar_libro(Libro("978-0-7432-7356-5", "1984", "George Orwell", "distopía", 1))

    # ── 3. Registrar usuarios ───────────────────────────
    separador("3. REGISTRO DE USUARIOS")
    usuarios = [
        Usuario("Ana García",    "U001"),
        Usuario("Carlos López",  "U002"),
        Usuario("María Fernández","U003"),
    ]
    for u in usuarios:
        bib.registrar_usuario(u)

    # Intentar registrar ID duplicado
    print()
    bib.registrar_usuario(Usuario("Otro Nombre", "U001"))

    # ── 4. Catálogo inicial ─────────────────────────────
    separador("4. CATÁLOGO COMPLETO")
    bib.mostrar_catalogo()

    # ── 5. Préstamos ────────────────────────────────────
    separador("5. PRÉSTAMOS")
    bib.prestar_libro("U001", "978-0-7432-7356-5")   # Ana toma 1984
    bib.prestar_libro("U001", "978-0-06-112008-4")   # Ana toma Matar a un ruiseñor
    bib.prestar_libro("U002", "978-0-7432-7356-5")   # Carlos toma 1984
    bib.prestar_libro("U003", "978-3-16-148410-0")   # María toma Cien años de soledad
    bib.prestar_libro("U002", "978-0-7432-7356-5")   # Carlos intenta otra copia de 1984
    bib.prestar_libro("U003", "978-0-7432-7356-5")   # María intenta 1984 (sin copias)

    # ── 6. Libros prestados por usuario ─────────────────
    separador("6. LIBROS EN PRÉSTAMO POR USUARIO")
    bib.listar_prestamos_usuario("U001")
    bib.listar_prestamos_usuario("U002")
    bib.listar_prestamos_usuario("U003")

    # ── 7. Búsquedas ────────────────────────────────────
    separador("7. BÚSQUEDAS EN EL CATÁLOGO")

    print("\n  🔍 Por título ('ruiseñor'):")
    for r in bib.buscar_por_titulo("ruiseñor"):
        print(f"      → {r.titulo} ({r.autor})")

    print("\n  🔍 Por autor ('Harper Lee'):")
    for r in bib.buscar_por_autor("Harper Lee"):
        print(f"      → {r.titulo}")

    print("\n  🔍 Por categoría ('ficción'):")
    for r in bib.buscar_por_categoria("ficción"):
        print(f"      → {r.titulo} — {r.autor}")

    print("\n  🔍 Búsqueda sin resultados ('terror'):")
    resultado = bib.buscar_por_categoria("terror")
    print(f"      Resultados: {resultado}")

    # ── 8. Devoluciones ─────────────────────────────────
    separador("8. DEVOLUCIONES")
    bib.devolver_libro("U001", "978-0-7432-7356-5")  # Ana devuelve 1984
    bib.devolver_libro("U003", "978-3-16-148410-0")  # María devuelve Cien años
    bib.devolver_libro("U002", "978-0-06-112008-4")  # Carlos intenta devolver algo que no tiene

    # ── 9. Estado tras devoluciones ─────────────────────
    separador("9. CATÁLOGO TRAS DEVOLUCIONES")
    bib.mostrar_catalogo()

    # ── 10. Historial ───────────────────────────────────
    separador("10. HISTORIAL COMPLETO DE USUARIOS")
    bib.listar_historial_usuario("U001")
    bib.listar_historial_usuario("U003")

    # ── 11. Dar de baja usuario con libros pendientes ───
    separador("11. BAJA DE USUARIOS")
    bib.dar_baja_usuario("U001")   # Aún tiene 'Matar a un ruiseñor'
    bib.devolver_libro("U001", "978-0-06-112008-4")  # Devuelve
    bib.dar_baja_usuario("U001")   # Ahora sí

    # ── 12. Quitar libro prestado ───────────────────────
    separador("12. QUITAR LIBRO DEL CATÁLOGO")
    bib.quitar_libro("978-0-7432-7356-5")  # 1984 tiene copias prestadas a U002
    bib.devolver_libro("U002", "978-0-7432-7356-5")
    bib.devolver_libro("U002", "978-0-7432-7356-5")  # 2ª copia que tomó Carlos
    bib.quitar_libro("978-0-7432-7356-5")  # Ahora sí

    separador("13. CATÁLOGO FINAL")
    bib.mostrar_catalogo()

    print("\n  ✅ Pruebas completadas.\n")