import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# ──────────────────────────────────────────────────────────────
# Ventana principal
# ──────────────────────────────────────────────────────────────
ventana = tk.Tk()
ventana.title("Agenda Personal")
ventana.geometry("700x480")
ventana.resizable(False, False)

# Lista en memoria que almacena los eventos agregados
eventos = []

# ──────────────────────────────────────────────────────────────
# FRAME 1 – Lista de eventos (parte superior)
# ──────────────────────────────────────────────────────────────
frame_lista = tk.Frame(ventana, bd=2, relief="groove", padx=10, pady=10)
frame_lista.pack(fill="both", expand=True, padx=10, pady=(10, 5))

# Etiqueta del área de la lista
tk.Label(frame_lista, text="Eventos programados", font=("Arial", 11, "bold")).pack(anchor="w")

# TreeView con columnas: Fecha, Hora, Descripción
tree = ttk.Treeview(
    frame_lista,
    columns=("fecha", "hora", "descripcion"),
    show="headings",
    height=8
)

# Definición de encabezados y ancho de cada columna
tree.heading("fecha",       text="Fecha")
tree.heading("hora",        text="Hora")
tree.heading("descripcion", text="Descripción")
tree.column("fecha",        width=110, anchor="center")
tree.column("hora",         width=80,  anchor="center")
tree.column("descripcion",  width=440, anchor="w")

# Scrollbar vertical para el TreeView
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ──────────────────────────────────────────────────────────────
# FRAME 2 – Campos de entrada (parte media)
# ──────────────────────────────────────────────────────────────
frame_entrada = tk.Frame(ventana, bd=2, relief="groove", padx=10, pady=10)
frame_entrada.pack(fill="x", padx=10, pady=5)

# ── Campo: Fecha ──
tk.Label(frame_entrada, text="Fecha:").grid(row=0, column=0, sticky="w", padx=5)

# DateEntry es el DatePicker de tkcalendar que muestra un calendario desplegable
entry_fecha = DateEntry(
    frame_entrada,
    width=14,
    date_pattern="dd/mm/yyyy"   # formato día/mes/año
)
entry_fecha.grid(row=0, column=1, padx=5, pady=4, sticky="w")

# ── Campo: Hora ──
tk.Label(frame_entrada, text="Hora (HH:MM):").grid(row=0, column=2, sticky="w", padx=5)

entry_hora = tk.Entry(frame_entrada, width=8)
entry_hora.insert(0, "08:00")   # valor inicial de ejemplo
entry_hora.grid(row=0, column=3, padx=5, pady=4, sticky="w")

# ── Campo: Descripción ──
tk.Label(frame_entrada, text="Descripción:").grid(row=0, column=4, sticky="w", padx=5)

entry_descripcion = tk.Entry(frame_entrada, width=28)
entry_descripcion.grid(row=0, column=5, padx=5, pady=4, sticky="w")

# ──────────────────────────────────────────────────────────────
# FRAME 3 – Botones de acción (parte inferior)
# ──────────────────────────────────────────────────────────────
frame_botones = tk.Frame(ventana, padx=10, pady=8)
frame_botones.pack(fill="x", padx=10, pady=(0, 10))

# ──────────────────────────────────────────────────────────────
# FUNCIONES DE LOS BOTONES
# ──────────────────────────────────────────────────────────────

def agregar_evento():
    """Lee los campos de entrada y agrega el evento al TreeView y a la lista."""
    fecha       = entry_fecha.get().strip()
    hora        = entry_hora.get().strip()
    descripcion = entry_descripcion.get().strip()

    # Validación: los tres campos deben tener contenido
    if not fecha or not hora or not descripcion:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    # Guarda el evento en la lista interna
    eventos.append({"fecha": fecha, "hora": hora, "descripcion": descripcion})

    # Inserta la nueva fila al final del TreeView
    tree.insert("", "end", values=(fecha, hora, descripcion))

    # Limpia los campos de hora y descripción para el siguiente ingreso
    entry_hora.delete(0, "end")
    entry_hora.insert(0, "08:00")
    entry_descripcion.delete(0, "end")


def eliminar_evento():
    """Elimina el evento seleccionado en el TreeView, previa confirmación."""
    seleccion = tree.selection()   # obtiene el ítem seleccionado

    if not seleccion:
        messagebox.showinfo("Sin selección", "Selecciona un evento de la lista.")
        return

    # Diálogo de confirmación antes de borrar
    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Deseas eliminar el evento seleccionado?"
    )

    if confirmar:
        item = seleccion[0]
        indice = tree.index(item)    # posición del ítem en el TreeView
        tree.delete(item)            # elimina la fila del TreeView
        del eventos[indice]          # elimina el dato de la lista interna


def salir():
    """Cierra la aplicación."""
    ventana.destroy()


# ──────────────────────────────────────────────────────────────
# Creación de los botones con sus comandos
# ──────────────────────────────────────────────────────────────

# Botón Agregar Evento
btn_agregar = tk.Button(
    frame_botones,
    text="Agregar Evento",
    width=20,
    bg="#4CAF50", fg="white",
    command=agregar_evento        # llama a la función agregar_evento al hacer clic
)
btn_agregar.pack(side="left", padx=8)

# Botón Eliminar Evento Seleccionado
btn_eliminar = tk.Button(
    frame_botones,
    text="Eliminar Evento Seleccionado",
    width=26,
    bg="#F44336", fg="white",
    command=eliminar_evento       # llama a la función eliminar_evento al hacer clic
)
btn_eliminar.pack(side="left", padx=8)

# Botón Salir
btn_salir = tk.Button(
    frame_botones,
    text="Salir",
    width=10,
    bg="#9E9E9E", fg="white",
    command=salir                 # cierra la ventana al hacer clic
)
btn_salir.pack(side="right", padx=8)

# ──────────────────────────────────────────────────────────────
# Inicia el bucle principal de la interfaz gráfica
# ──────────────────────────────────────────────────────────────
ventana.mainloop()