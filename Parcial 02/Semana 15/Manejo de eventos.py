import tkinter as tk
from tkinter import messagebox

# Colores pastel
BG       = "#fdf6f0"
PANEL    = "#fce4ec"
ACCENT   = "#f48fb1"
ACCENT2  = "#b39ddb"
TEXT     = "#4a4a4a"
DONE_FG  = "#81c784"
DONE_BG  = "#e8f5e9"

# Fuentes
FONT     = ("Segoe UI", 11)
FONT_B   = ("Segoe UI", 11, "bold")
FONT_T   = ("Segoe UI", 17, "bold")
FONT_S   = ("Segoe UI", 9)

# Lista de tareas en memoria
tareas = []  # Cada elemento es un diccionario {"texto": str, "completada": bool}


# ── Funciones manejadoras de eventos ──────────────────────────────────────────

def añadir_tarea(event=None):
    """Añade una nueva tarea a la lista. Se llama con el botón o con Enter."""
    texto = entrada_var.get().strip()
    if not texto:
        messagebox.showwarning("Campo vacío", "Escribe una tarea antes de añadirla.")
        return
    tareas.append({"texto": texto, "completada": False})
    entrada_var.set("")
    entrada.focus()
    actualizar_lista()

def marcar_completada():
    """Marca o desmarca la tarea seleccionada como completada."""
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona una tarea de la lista.")
        return
    i = seleccion[0]
    tareas[i]["completada"] = not tareas[i]["completada"]  # Alterna True/False
    actualizar_lista()
    listbox.selection_set(i)  # Mantiene la selección después de actualizar

def eliminar_tarea():
    """Elimina la tarea seleccionada de la lista."""
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona una tarea de la lista.")
        return
    i = seleccion[0]
    tareas.pop(i)
    actualizar_lista()

def doble_clic(event):
    """Evento adicional: doble clic en una tarea para marcarla como completada."""
    marcar_completada()

def actualizar_lista():
    """Redibuja el Listbox con el estado actual de todas las tareas."""
    listbox.delete(0, "end")
    for t in tareas:
        prefijo = "✔  " if t["completada"] else "○  "
        listbox.insert("end", f"  {prefijo}{t['texto']}")
        if t["completada"]:
            idx = listbox.size() - 1
            listbox.itemconfig(idx, fg=DONE_FG, bg=DONE_BG)


# ── Construcción de la ventana ────────────────────────────────────────────────

ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("600x480")
ventana.resizable(False, False)
ventana.configure(bg=BG)

# Título
tk.Label(ventana, text="🌸 Gestor de Tareas", font=FONT_T,
         bg=BG, fg=ACCENT).pack(pady=(16, 8))

# Campo de entrada
frame_entrada = tk.Frame(ventana, bg=PANEL, padx=12, pady=10,
                         highlightbackground=ACCENT, highlightthickness=2)
frame_entrada.pack(fill="x", padx=24, pady=(0, 10))

tk.Label(frame_entrada, text="Nueva tarea:", font=FONT_S,
         bg=PANEL, fg="#b0a0aa").pack(anchor="w")

fila = tk.Frame(frame_entrada, bg=PANEL)
fila.pack(fill="x", pady=(4, 0))

entrada_var = tk.StringVar()
entrada = tk.Entry(fila, textvariable=entrada_var, font=FONT,
                   bg="white", fg=TEXT, relief="flat",
                   highlightthickness=2, highlightcolor=ACCENT,
                   highlightbackground="#f8bbd0")
entrada.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
entrada.focus()

# Evento: presionar Enter en el campo de texto añade la tarea
entrada.bind("<Return>", añadir_tarea)

tk.Button(fila, text="＋ Añadir", command=añadir_tarea, font=FONT_B,
          bg=ACCENT, fg="white", relief="flat", padx=10, pady=5,
          cursor="hand2").pack(side="left")

# Lista de tareas
frame_lista = tk.Frame(ventana, bg=PANEL, padx=12, pady=10,
                       highlightbackground="#f8bbd0", highlightthickness=2)
frame_lista.pack(fill="both", expand=True, padx=24, pady=(0, 10))

sb = tk.Scrollbar(frame_lista)
sb.pack(side="right", fill="y")

listbox = tk.Listbox(frame_lista, yscrollcommand=sb.set, font=FONT,
                     bg="#fffaf7", fg=TEXT, selectbackground="#ce93d8",
                     selectforeground="white", relief="flat",
                     highlightthickness=0, selectmode="single", cursor="hand2")
listbox.pack(fill="both", expand=True)
sb.config(command=listbox.yview)

# Evento adicional: doble clic en una tarea para marcarla como completada
listbox.bind("<Double-Button-1>", doble_clic)

# Botones de acción
frame_botones = tk.Frame(ventana, bg=BG)
frame_botones.pack(fill="x", padx=24, pady=(0, 16))

tk.Button(frame_botones, text="✔  Marcar como Completada",
          command=marcar_completada, font=FONT_B,
          bg=ACCENT2, fg="white", relief="flat", padx=10, pady=6,
          cursor="hand2").pack(side="left", padx=(0, 8))

tk.Button(frame_botones, text="✖  Eliminar Tarea",
          command=eliminar_tarea, font=FONT_B,
          bg="#ef9a9a", fg="white", relief="flat", padx=10, pady=6,
          cursor="hand2").pack(side="left")

ventana.mainloop()