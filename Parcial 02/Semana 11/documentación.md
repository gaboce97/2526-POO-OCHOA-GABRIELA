Sistema de Gestión de Inventario para Tienda

Autor: Gabriela Ochoa
Materia: Programación Orientada a Objetos

DESCRIPCIÓN GENERAL

Este programa implementa un sistema de gestión de inventario para una tienda,
desarrollado en Python aplicando los principios de la Programación Orientada
a Objetos (POO). Permite al usuario agregar, eliminar, actualizar y buscar
productos desde un menú interactivo en consola. Toda la información se guarda
automáticamente en un archivo externo para que los datos persistan entre
ejecuciones del programa.

ARCHIVOS DEL PROYECTO

  inventario.py        →  Código fuente principal del sistema
  documentacion.py     →  Este archivo (explicación del funcionamiento)
  inventario.json      →  Archivo de datos generado automáticamente al ejecutar

- ESTRUCTURA DEL PROGRAMA — CLASES

documentacion_clases = """
CLASE: Producto
───────────────
Representa un artículo individual dentro del inventario.

Atributos (todos privados con doble guion bajo para encapsulamiento):
  __id_producto  (str)    → Identificador único. No puede repetirse.
  __nombre       (str)    → Nombre descriptivo del producto.
  __cantidad     (int)    → Número de unidades disponibles en stock.
  __precio       (float)  → Precio unitario en dólares.

Métodos:
  Getters → get_id(), get_nombre(), get_cantidad(), get_precio()
            Permiten leer los atributos privados desde fuera de la clase.

  Setters → set_nombre(), set_cantidad(), set_precio()
            Modifican los atributos con validación:
              - El nombre no puede estar vacío.
              - La cantidad no puede ser negativa.
              - El precio no puede ser negativo.
            Si alguna regla se viola, se lanza un ValueError.

  a_diccionario() → Convierte el objeto Producto en un diccionario de Python,
                    necesario para poder guardarlo en el archivo JSON.
                    Ejemplo:
                      {"id": "1", "nombre": "Arroz", "cantidad": 50, "precio": 2.75}

  a_tupla()       → Devuelve una tupla inmutable con todos los datos del producto.
                    Útil como snapshot del estado en un momento dado.
                    Ejemplo:
                      ("1", "Arroz", 50, 2.75)

  __str__()       → Define cómo se imprime el producto en consola con formato tabla.

──────────────────────────────────────────────────────────────────────────────

CLASE: Inventario
─────────────────
Es el núcleo del sistema. Gestiona la colección de productos y el archivo.

Métodos:
  agregar_producto(id, nombre, cantidad, precio)
      Crea un objeto Producto y lo agrega al inventario. Antes verifica que
      el ID no esté ya en uso. Guarda los cambios automáticamente.

  eliminar_producto(id)
      Busca el producto por ID y lo elimina del inventario. Guarda los cambios.

  actualizar_producto(id, nueva_cantidad, nuevo_precio)
      Modifica la cantidad y/o el precio de un producto existente.
      Cada campo es opcional: si se deja vacío, no se modifica.

  buscar_por_nombre(termino)
      Recorre todos los productos y devuelve una lista con aquellos cuyo
      nombre contiene el término buscado (sin distinción de mayúsculas).

  mostrar_todos()
      Imprime todos los productos en formato de tabla en la consola.

  guardar_en_archivo()
      Convierte el inventario a una lista de diccionarios y lo escribe
      en el archivo "inventario.json" usando el módulo json.

  cargar_desde_archivo()
      Al iniciar el programa, lee el archivo JSON y reconstruye los
      objetos Producto, restaurando el estado anterior del inventario.
"""

- USO DE COLECCIONES

documentacion_colecciones = """
El programa utiliza cuatro tipos de colecciones de Python, cada una elegida
por sus características específicas:

┌─────────────┬──────────────────────────────┬────────────────────────────────┐
│ Colección   │ Dónde se usa                 │ Por qué se eligió              │
├─────────────┼──────────────────────────────┼────────────────────────────────┤
│ dict        │ Almacén principal            │ Acceso por clave (ID) en O(1)  │
│             │ self.__productos             │ Sin necesidad de recorrer todo │
├─────────────┼──────────────────────────────┼────────────────────────────────┤
│ set         │ Registro de IDs únicos       │ Verificar duplicados en O(1)   │
│             │ self.__ids_usados            │ Garantiza IDs no repetidos     │
├─────────────┼──────────────────────────────┼────────────────────────────────┤
│ list        │ Resultados de búsqueda       │ Colección ordenada y temporal  │
│             │ retorno de buscar_por_nombre │ Ideal para recorrer resultados │
├─────────────┼──────────────────────────────┼────────────────────────────────┤
│ tuple       │ Snapshot de un producto      │ Inmutable: no se puede alterar │
│             │ método a_tupla()             │ accidentalmente                │
└─────────────┴──────────────────────────────┴────────────────────────────────┘

DETALLE DE CADA COLECCIÓN:

1. DICCIONARIO (dict) — Almacén principal
   ----------------------------------------
   self.__productos = {}   →  clave: ID del producto | valor: objeto Producto

   Razón de uso:
   Los diccionarios permiten acceder a cualquier producto directamente por su
   ID sin recorrer toda la colección. Esto es fundamental cuando el inventario
   tiene muchos productos y se necesita eficiencia.

   Ejemplo de contenido interno:
     {
       "1": <Producto: Arroz>,
       "2": <Producto: Aceite>,
       "3": <Producto: Leche>
     }

2. CONJUNTO (set) — Registro de IDs
   ----------------------------------
   self.__ids_usados = set()

   Razón de uso:
   Antes de agregar un producto, el programa verifica si el ID ya existe.
   Hacer esta verificación en un set es O(1) (instantáneo), mientras que
   hacerlo buscando en el diccionario sería menos directo.
   Además, por definición un set no permite elementos repetidos, lo que
   refuerza la unicidad de los IDs.

   Ejemplo de contenido interno:
     {"P001", "P002", "P003"}

3. LISTA (list) — Resultados de Búsqueda
   -----------------------------------------
   resultados = [p for p in self.__productos.values() if termino in p.get_nombre().lower()]

   Razón de uso:
   La búsqueda puede devolver varios productos que coincidan con el término.
   Una lista permite almacenarlos en orden, recorrerlos e imprimirlos
   fácilmente. Se construye usando comprensión de listas (list comprehension),
   una forma concisa y eficiente de filtrar elementos.

4. TUPLA (tuple) — Snapshot Inmutable
   --------------------------------------
   return (self.__id_producto, self.__nombre, self.__cantidad, self.__precio)

   Razón de uso:
   A diferencia de una lista, una tupla no puede modificarse después de
   ser creada. Esto la hace ideal para representar el estado de un producto
   en un momento específico (snapshot), sin riesgo de alterarlo por error.
"""

- ALMACENAMIENTO EN ARCHIVOS

documentacion_archivos = """
El programa usa el módulo estándar 'json' para guardar y cargar el inventario.
El archivo generado se llama: inventario.json

── GUARDAR (guardar_en_archivo) ────────────────────────────────────────────

Cada vez que el inventario cambia (agregar, eliminar, actualizar), el programa
llama automáticamente a este método. El proceso es:

  Paso 1: Convertir cada objeto Producto a un diccionario con a_diccionario()
  Paso 2: Armar una lista con todos esos diccionarios
  Paso 3: Escribir esa lista en el archivo JSON con json.dump()

Código resumido:
  datos = [p.a_diccionario() for p in self.__productos.values()]
  with open("inventario.json", "w", encoding="utf-8") as archivo:
      json.dump(datos, archivo, ensure_ascii=False, indent=4)

Ejemplo de cómo queda el archivo inventario.json:
  [
      {
          "id": "P001",
          "nombre": "Arroz integral",
          "cantidad": 50,
          "precio": 2.75
      },
      {
          "id": "P002",
          "nombre": "Aceite de oliva",
          "cantidad": 20,
          "precio": 8.99
      }
  ]

── CARGAR (cargar_desde_archivo) ──────────────────────────────────────────

Al iniciar el programa, este método se ejecuta automáticamente en el
constructor (__init__) de la clase Inventario. El proceso es:

  Paso 1: Verificar si el archivo inventario.json existe en el sistema
  Paso 2: Leer el archivo y convertirlo de JSON a lista de diccionarios (json.load)
  Paso 3: Por cada diccionario, crear un objeto Producto y agregarlo al dict y al set

Código resumido:
  with open("inventario.json", "r", encoding="utf-8") as archivo:
      datos = json.load(archivo)
  for d in datos:
      producto = Producto(d["id"], d["nombre"], d["cantidad"], d["precio"])
      self.__productos[d["id"]] = producto
      self.__ids_usados.add(d["id"])

Casos especiales manejados:
  - Si el archivo no existe (primera ejecución): el inventario inicia vacío sin error.
  - Si el archivo está corrupto: se captura el error y se inicia vacío con aviso.
"""
 
  - CONCEPTOS DE POO APLICADOS


documentacion_poo = """
ENCAPSULAMIENTO
  Todos los atributos de la clase Producto son privados (prefijo __).
  Solo se pueden leer o modificar mediante getters y setters, que incluyen
  validaciones para proteger la integridad de los datos.

ABSTRACCIÓN
  La clase Inventario oculta completamente la implementación interna
  (el diccionario y el conjunto). El usuario del objeto solo necesita llamar
  métodos como agregar_producto() o buscar_por_nombre() sin conocer cómo
  están organizados los datos internamente.

MODULARIDAD
  Las funciones de menú (menu_agregar, menu_eliminar, etc.) están separadas
  de la lógica de negocio de las clases. Esto facilita modificar la interfaz
  sin tocar la lógica del inventario, y viceversa.

VALIDACIÓN CON EXCEPCIONES
  Los setters lanzan ValueError si los datos no son válidos. El menú
  principal captura estas excepciones con try/except para mostrar mensajes
  amigables sin interrumpir el programa.
"""


- MENÚ INTERACTIVO

documentacion_menu = """
El menú se muestra en un bucle while True que solo termina cuando el usuario
elige la opción "6. Salir".

Las opciones están mapeadas en un DICCIONARIO DE FUNCIONES:
  opciones = {
      "1": menu_agregar,
      "2": menu_eliminar,
      "3": menu_actualizar,
      "4": menu_buscar,
      "5": lambda inv: inv.mostrar_todos(),
  }

Esto evita una larga cadena de if/elif y hace que agregar nuevas opciones
en el futuro sea muy sencillo: solo se añade una entrada al diccionario.

Apariencia del menú en consola:
  ═════════════════════════════════════════════
     SISTEMA DE GESTIÓN DE INVENTARIO
  ═════════════════════════════════════════════
    1. Agregar producto
    2. Eliminar producto
    3. Actualizar producto
    4. Buscar producto por nombre
    5. Mostrar todos los productos
    6. Salir
  ═════════════════════════════════════════════
"""



- CÓMO EJECUTAR EL PROGRAMA
documentacion_ejecucion = """
Requisitos:
  - Python 3.8 o superior
  - No se requieren librerías externas (solo módulos estándar: json, os)

Desde la terminal o desde PyCharm:
  python inventario.py

Al ejecutarlo por primera vez, el inventario estará vacío y se creará el
archivo inventario.json automáticamente cuando se agregue el primer producto.
En ejecuciones posteriores, el inventario se restaurará con los datos guardados.
"""


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA — Imprime toda la documentación al ejecutar este archivo
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    secciones = [
        ("1. CLASES Y MÉTODOS",        documentacion_clases),
        ("2. USO DE COLECCIONES",       documentacion_colecciones),
        ("3. ALMACENAMIENTO EN ARCHIVOS", documentacion_archivos),
        ("4. CONCEPTOS DE POO",         documentacion_poo),
        ("5. MENÚ INTERACTIVO",         documentacion_menu),
        ("6. CÓMO EJECUTAR",            documentacion_ejecucion),
    ]

    print(__doc__)  # Imprime el encabezado del módulo
    for titulo, contenido in secciones:
        print(f"\n{'═' * 78}")
        print(f"  {titulo}")
        print('═' * 78)
        print(contenido)