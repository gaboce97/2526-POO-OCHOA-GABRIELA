import os
import subprocess
from datetime import datetime

# ============================================================================
# ADAPTACIÓN PERSONAL - Dashboard POO Mejorado
# Autor: Gabriela (2526-POO-OCHOA-GABRIELA)
# Fecha de Adaptación: 2026
#
# CAMBIOS REALIZADOS:
# 1. Agregué un sistema de bienvenida personalizado con fecha y hora
# 2. Adaptado para trabajar con carpetas Semana_02 a Semana_08
# 3. Agregué validación mejorada de entrada de usuario
# 4. Agregué estadísticas de navegación (cuántos scripts se vieron)
# 5. Mejoré los mensajes de error con más claridad
# 6. Agregué función para contar y mostrar total de scripts
# 7. Mejoré la visualización con separadores y colores de texto
# 8. Agregué opción de búsqueda rápida de scripts por nombre
# 9. Ahora busca automáticamente las carpetas Semana_XX en el directorio
# 10. CORRECCIÓN: Mejorado el sistema de detección de carpetas
# ============================================================================

# CAMBIO 1: Variable global para llevar estadísticas
scripts_visitados = 0
total_scripts_encontrados = 0


def mostrar_bienvenida():
    """
    CAMBIO 1: Nueva función agregada
    Muestra un mensaje de bienvenida personalizado con la fecha y hora actual.
    Esto mejora la experiencia del usuario al iniciar el dashboard.
    """
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("\n" + "=" * 60)
    print("  BIENVENIDO AL DASHBOARD - POO 2526")
    print("  Estructura de Semanas (02-08)")
    print("=" * 60)
    print(f"  Fecha y Hora: {fecha_actual}")
    print("=" * 60 + "\n")


def obtener_semanas_disponibles(ruta_base):
    """
    CAMBIO 9: Nueva función agregada
    CAMBIO 10: Corrección mejorada para detectar carpetas
    Busca automáticamente todas las carpetas "Semana_XX" en el directorio.
    Retorna un diccionario con las semanas disponibles.
    """
    semanas = {}
    print(f"📂 Buscando carpetas en: {ruta_base}")

    try:
        # Listar todos los items en el directorio
        items = os.listdir(ruta_base)
        print(f"📊 Items encontrados: {items}\n")

        for item in items:
            ruta_item = os.path.join(ruta_base, item)

            # Debug: mostrar qué se está evaluando
            es_directorio = os.path.isdir(ruta_item)
            empieza_con_semana = item.lower().startswith("semana")

            print(f"   Evaluando: {item}")
            print(f"      - ¿Es directorio?: {es_directorio}")
            print(f"      - ¿Empieza con 'Semana'?: {empieza_con_semana}")

            # Buscar carpetas que empiezan con "Semana" (case-insensitive)
            if es_directorio and empieza_con_semana:
                # Extrae el número de "Semana_XX" o "SemanaXX"
                try:
                    numero = ''.join(filter(str.isdigit, item))
                    if numero:  # Solo si encuentra números
                        semanas[numero] = item
                        print(f"      ✓ ENCONTRADA: {item} (Número: {numero})\n")
                    else:
                        print(f"      ✗ Sin número en el nombre\n")
                except Exception as e:
                    print(f"      ✗ Error: {e}\n")
            else:
                print(f"      ✗ No cumple criterios\n")

    except Exception as e:
        print(f"❌ Error al buscar semanas: {e}")

    # Ordenar numéricamente
    resultado = dict(sorted(semanas.items(), key=lambda x: int(x[0])))
    print(f"✓ Semanas encontradas: {resultado}\n")
    return resultado


def mostrar_codigo(ruta_script):
    """
    Función original mejorada con mejor manejo de errores y feedback.
    Asegúrate de que la ruta al script es absoluta.
    """
    global scripts_visitados  # CAMBIO 2: Rastrear scripts visitados

    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n{'=' * 60}")
            print(f"  CÓDIGO DE: {os.path.basename(ruta_script)}")
            print(f"{'=' * 60}\n")
            print(codigo)
            print(f"\n{'=' * 60}\n")

            # CAMBIO 2: Incrementar contador de scripts visitados
            scripts_visitados += 1

            return codigo
    except FileNotFoundError:
        # CAMBIO 3: Mensaje de error mejorado
        print(f"\n❌ ERROR: No se encontró el archivo '{os.path.basename(ruta_script)}'")
        print(f"   Ruta: {ruta_script_absoluta}\n")
        return None
    except Exception as e:
        # CAMBIO 3: Mensaje de error más descriptivo
        print(f"\n❌ ERROR al leer el archivo: {e}\n")
        return None


def ejecutar_codigo(ruta_script):
    """
    Función original mejorada con mejor feedback del usuario.
    Ejecuta un script Python en una ventana separada.
    """
    try:
        if os.name == 'nt':  # Windows
            # CAMBIO 4: Agregar mensaje de confirmación
            print("\n✓ Abriendo script en nueva ventana de comando...")
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            print("\n✓ Abriendo script en nueva terminal...")
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        # CAMBIO 3: Mensaje de error mejorado
        print(f"\n❌ Error al ejecutar el código: {e}\n")


def buscar_script(scripts, busqueda):
    """
    CAMBIO 5: Nueva función agregada
    Permite buscar scripts por nombre sin necesidad de navegar manualmente.
    Retorna una lista de scripts que coinciden con la búsqueda.
    """
    resultados = [s for s in scripts if busqueda.lower() in s.lower()]
    return resultados


def contar_scripts_totales(ruta_base):
    """
    CAMBIO 6: Nueva función agregada
    Calcula el total de scripts Python en el proyecto.
    Útil para tener una visión general del proyecto.
    """
    total = 0
    for root, dirs, files in os.walk(ruta_base):
        for file in files:
            if file.endswith('.py'):
                total += 1
    return total


def mostrar_menu():
    """
    Función principal mejorada.
    CAMBIO IMPORTANTE: Ahora busca automáticamente las carpetas Semana_XX
    """
    # CAMBIO 1: Mostrar bienvenida al iniciar
    mostrar_bienvenida()

    ruta_base = os.path.dirname(__file__)
    print(f"📍 Directorio base del Dashboard: {ruta_base}\n")

    # CAMBIO 9 y 10: Obtener semanas disponibles automáticamente
    semanas = obtener_semanas_disponibles(ruta_base)

    if not semanas:
        print("❌ No se encontraron carpetas Semana_XX en esta ruta.")
        print(f"   Ruta: {ruta_base}")
        print("\n   Verifica que el Dashboard- Semana 08.py esté en la carpeta Parcial_01")
        print("   junto con las carpetas Semana_02, Semana_03, etc.")
        return

    # CAMBIO 8: Calcular y mostrar total de scripts al inicio
    try:
        total = contar_scripts_totales(ruta_base)
        print(f"📊 Total de scripts encontrados: {total}\n")
    except:
        pass

    while True:
        print("\n" + "=" * 60)
        print("  MENÚ PRINCIPAL - DASHBOARD")
        print("=" * 60)

        # CAMBIO 9: Mostrar las semanas encontradas dinámicamente
        print("  Semanas disponibles:")
        for key in sorted(semanas.keys()):
            print(f"  {key} - {semanas[key]}")
        print("  0 - Salir del Dashboard")
        print("=" * 60)

        # CAMBIO 10: Mensaje de elección mejorado
        print(f"\n📝 Scripts visitados en esta sesión: {scripts_visitados}")
        eleccion_semana = input("\n👉 Elige una semana o '0' para salir: ").strip()

        if eleccion_semana == '0':
            # CAMBIO 11: Mensaje de despedida personalizado
            print(f"\n{'=' * 60}")
            print(f"  ¡Hasta luego! Visitaste {scripts_visitados} scripts en esta sesión.")
            print(f"{'=' * 60}\n")
            break
        elif eleccion_semana in semanas:
            ruta_semana = os.path.join(ruta_base, semanas[eleccion_semana])
            # CAMBIO 12: Validar que la carpeta exista
            if os.path.exists(ruta_semana):
                mostrar_contenido_semana(ruta_semana, semanas[eleccion_semana])
            else:
                print(f"\n❌ La carpeta '{semanas[eleccion_semana]}' no existe en esta ruta.")
        else:
            print("\n❌ Opción no válida. Por favor, intenta de nuevo.")


def mostrar_contenido_semana(ruta_semana, nombre_semana):
    """
    CAMBIO IMPORTANTE: Nueva función que reemplaza mostrar_sub_menu
    Muestra el contenido de una semana (puede ser archivos directos o subcarpetas).
    """
    try:
        # Obtener tanto archivos como subcarpetas
        items = []
        subcarpetas = []
        scripts_directos = []

        for item in os.listdir(ruta_semana):
            ruta_item = os.path.join(ruta_semana, item)
            if os.path.isdir(ruta_item):
                subcarpetas.append(item)
            elif item.endswith('.py'):
                scripts_directos.append(item)

        items = subcarpetas + scripts_directos

        if not items:
            print(f"\n⚠️  No hay contenido en '{nombre_semana}'")
            return

        while True:
            print(f"\n{'=' * 60}")
            print(f"  CONTENIDO - {nombre_semana}")
            print(f"{'=' * 60}")

            for i, item in enumerate(items, start=1):
                tipo = "📁 Carpeta" if item in subcarpetas else "📄 Script"
                print(f"  {i} - {tipo}: {item}")
            print("  0 - Regresar al menú principal")
            print("=" * 60)

            eleccion = input("\n👉 Elige una opción o '0' para regresar: ").strip()

            if eleccion == '0':
                break
            else:
                try:
                    eleccion = int(eleccion) - 1
                    if 0 <= eleccion < len(items):
                        item_seleccionado = items[eleccion]
                        ruta_item = os.path.join(ruta_semana, item_seleccionado)

                        if item_seleccionado in subcarpetas:
                            # Es una carpeta, mostrar sus scripts
                            mostrar_scripts_en_carpeta(ruta_item, item_seleccionado)
                        else:
                            # Es un script, mostrarlo directamente
                            mostrar_y_ejecutar_script(ruta_item)
                    else:
                        print("\n❌ Opción no válida. Por favor, intenta de nuevo.")
                except ValueError:
                    print("\n❌ Por favor, ingresa un número válido.")
    except Exception as e:
        print(f"\n❌ Error al acceder a la carpeta: {e}")


def mostrar_scripts_en_carpeta(ruta_carpeta, nombre_carpeta):
    """
    CAMBIO IMPORTANTE: Nueva función
    Muestra los scripts dentro de una carpeta específica.
    """
    scripts = [f.name for f in os.scandir(ruta_carpeta) if f.is_file() and f.name.endswith('.py')]

    if not scripts:
        print(f"\n⚠️  No hay scripts Python en '{nombre_carpeta}'")
        return

    while True:
        print(f"\n{'=' * 60}")
        print(f"  SCRIPTS - {nombre_carpeta} ({len(scripts)} scripts)")
        print(f"{'=' * 60}")

        for i, script in enumerate(scripts, start=1):
            print(f"  {i} - {script}")
        print("  0 - Regresar al menú anterior")
        print("  b - Buscar un script por nombre")
        print("=" * 60)

        eleccion_script = input("\n👉 Elige un script, '0' para regresar o 'b' para buscar: ").strip()

        if eleccion_script.lower() == 'b':
            termino_busqueda = input("\n🔍 Escribe el nombre del script a buscar: ").strip()
            resultados = buscar_script(scripts, termino_busqueda)

            if resultados:
                print(f"\n✓ Se encontraron {len(resultados)} resultado(s):")
                for i, script in enumerate(resultados, start=1):
                    print(f"  {i} - {script}")
            else:
                print(f"\n❌ No se encontraron scripts con '{termino_busqueda}'")
            continue

        if eleccion_script == '0':
            break
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_carpeta, scripts[eleccion_script])
                    mostrar_y_ejecutar_script(ruta_script)
                else:
                    print("\n❌ Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("\n❌ Por favor, ingresa un número válido.")


def mostrar_y_ejecutar_script(ruta_script):
    """
    CAMBIO IMPORTANTE: Nueva función
    Muestra el código de un script y pregunta si ejecutarlo.
    """
    codigo = mostrar_codigo(ruta_script)

    if codigo:
        print("\n¿Desea ejecutar este script?")
        ejecutar = input("  Ingrese '1' para Sí o '0' para No: ").strip()

        if ejecutar == '1':
            ejecutar_codigo(ruta_script)
        elif ejecutar == '0':
            print("\n✓ Script no ejecutado.")
        else:
            print("\n❌ Opción no válida.")

        input("\n⏎ Presiona Enter para continuar...")


# ============================================================================
# Ejecutar el dashboard
# ============================================================================
if __name__ == "__main__":
    try:
        mostrar_menu()
    except KeyboardInterrupt:
        # CAMBIO 21: Mejor manejo cuando el usuario presiona Ctrl+C
        print("\n\n⚠️  Dashboard interrumpido por el usuario.")
        print("¡Hasta luego!\n")
    except Exception as e:
        # CAMBIO 22: Manejo de excepciones generales
        print(f"\n❌ Error inesperado: {e}\n")