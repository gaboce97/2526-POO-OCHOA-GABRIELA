"""
Gestor de Tareas — Aplicación GUI con Tkinter
==============================================
Atajos de teclado:
  Enter      → Añadir tarea
  C          → Marcar tarea seleccionada como completada
  Delete / D → Eliminar tarea seleccionada
  Escape     → Cerrar la aplicación
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox


# ─────────────────────────── PALETA DE COLORES ───────────────────────────────
BG          = "#1A1A2E"   # fondo principal (azul muy oscuro)
PANEL       = "#16213E"   # fondo del panel lateral
CARD        = "#0F3460"   # fondo de tarjetas / lista
ACCENT      = "#E94560"   # rojo-rosa de acento
ACCENT2     = "#F5A623"   # naranja para completadas
TEXT        = "#EAEAEA"   # texto principal
TEXT_SOFT   = "#8892A4"   # texto suave / placeholder
DONE_BG     = "#0D2137"   # fondo ítem completado
DONE_FG     = "#4CAF50"   # verde para completadas
HOVER       = "#1C3A5E"   # hover sobre lista
SEL         = "#E9456033" # selección (semi-transparente)


class GestorTareas:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✦ Gestor de Tareas")
        self.root.geometry("680x580")
        self.root.minsize(520, 420)
        self.root.configure(bg=BG)

        # Intentar icono (falla silenciosamente si no existe)
        try:
            self.root.iconbitmap("")
        except Exception:
            pass

        self._fuentes()
        self._construir_ui()
        self._atajos()

        # Estado
        self.tareas: list[dict] = []   # {"texto": str, "completada": bool}

    # ─────────────────────── FUENTES ─────────────────────────────────────────
    def _fuentes(self):
        self.f_titulo  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.f_subtit  = tkfont.Font(family="Segoe UI", size=9)
        self.f_entrada = tkfont.Font(family="Segoe UI", size=12)
        self.f_lista   = tkfont.Font(family="Segoe UI", size=11)
        self.f_btn     = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_badge   = tkfont.Font(family="Segoe UI", size=8, weight="bold")
        self.f_tip     = tkfont.Font(family="Segoe UI", size=8)

    # ─────────────────────── UI ──────────────────────────────────────────────
    def _construir_ui(self):
        # ── Cabecera ──────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=PANEL, padx=24, pady=14)
        header.pack(fill="x")

        tk.Label(
            header, text="✦ Gestor de Tareas",
            bg=PANEL, fg=TEXT, font=self.f_titulo
        ).pack(side="left")

        self.lbl_contador = tk.Label(
            header, text="0 tareas",
            bg=PANEL, fg=TEXT_SOFT, font=self.f_subtit
        )
        self.lbl_contador.pack(side="right", pady=4)

        # ── Separador decorativo ──────────────────────────────────────────────
        sep = tk.Frame(self.root, bg=ACCENT, height=2)
        sep.pack(fill="x")

        # ── Cuerpo principal ──────────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)

        # ── Fila de entrada ───────────────────────────────────────────────────
        row_input = tk.Frame(body, bg=BG)
        row_input.pack(fill="x", pady=(0, 14))

        self.entrada = tk.Entry(
            row_input,
            font=self.f_entrada,
            bg=CARD, fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            bd=0,
        )
        self.entrada.pack(side="left", fill="x", expand=True, ipady=10, ipadx=12)
        self.entrada.insert(0, "Escribe una nueva tarea...")
        self.entrada.config(fg=TEXT_SOFT)
        self.entrada.bind("<FocusIn>",  self._clear_placeholder)
        self.entrada.bind("<FocusOut>", self._restore_placeholder)

        # Borde redondeado simulado con canvas bajo la entrada
        self._borde_entrada(row_input)

        btn_add = self._boton(
            row_input, "＋ Añadir", ACCENT,
            command=self.añadir_tarea
        )
        btn_add.pack(side="left", padx=(10, 0), ipady=4, ipadx=10)

        # ── Lista de tareas ───────────────────────────────────────────────────
        frame_lista = tk.Frame(body, bg=CARD, padx=2, pady=2)
        frame_lista.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista, bg=CARD, troughcolor=CARD,
                                  activebackground=ACCENT, bd=0, width=8)
        scrollbar.pack(side="right", fill="y")

        self.lista = tk.Listbox(
            frame_lista,
            font=self.f_lista,
            bg=CARD, fg=TEXT,
            selectbackground=ACCENT,
            selectforeground=TEXT,
            activestyle="none",
            bd=0, highlightthickness=0,
            relief="flat",
            yscrollcommand=scrollbar.set,
            cursor="hand2",
        )
        self.lista.pack(fill="both", expand=True, padx=2, pady=2)
        scrollbar.config(command=self.lista.yview)

        # Hover
        self.lista.bind("<Motion>",    self._hover_lista)
        self.lista.bind("<Leave>",     lambda e: self._reset_hover())

        # ── Fila de botones de acción ─────────────────────────────────────────
        row_btns = tk.Frame(body, bg=BG)
        row_btns.pack(fill="x", pady=(12, 0))

        btn_done = self._boton(
            row_btns, "✔ Completar  [C]", DONE_FG,
            command=self.completar_tarea
        )
        btn_done.pack(side="left", ipady=4, ipadx=10, padx=(0, 8))

        btn_del = self._boton(
            row_btns, "✖ Eliminar  [Del]", ACCENT,
            command=self.eliminar_tarea
        )
        btn_del.pack(side="left", ipady=4, ipadx=10)

        btn_clear = self._boton(
            row_btns, "⊘ Limpiar completadas", TEXT_SOFT,
            command=self.limpiar_completadas, outlined=True
        )
        btn_clear.pack(side="right", ipady=4, ipadx=10)

        # ── Barra de atajos ───────────────────────────────────────────────────
        tips = tk.Frame(self.root, bg=PANEL, padx=20, pady=6)
        tips.pack(fill="x", side="bottom")

        atajos = [
            ("Enter", "añadir"),
            ("C", "completar"),
            ("Del / D", "eliminar"),
            ("Esc", "salir"),
        ]
        for tecla, accion in atajos:
            self._badge_atajo(tips, tecla, accion)

    # ─────────────── helpers UI ──────────────────────────────────────────────
    def _boton(self, parent, texto, color, command=None, outlined=False):
        if outlined:
            btn = tk.Button(
                parent, text=texto, font=self.f_btn,
                bg=PANEL, fg=color,
                activebackground=HOVER, activeforeground=color,
                relief="flat", bd=1, cursor="hand2",
                highlightbackground=color, highlightthickness=1,
                command=command
            )
        else:
            btn = tk.Button(
                parent, text=texto, font=self.f_btn,
                bg=color, fg="#FFFFFF",
                activebackground=self._oscurecer(color), activeforeground="#FFFFFF",
                relief="flat", bd=0, cursor="hand2",
                command=command
            )
        return btn

    def _badge_atajo(self, parent, tecla, accion):
        frame = tk.Frame(parent, bg=PANEL)
        frame.pack(side="left", padx=10)
        tk.Label(
            frame, text=tecla,
            bg=CARD, fg=ACCENT,
            font=self.f_badge, padx=5, pady=1
        ).pack(side="left")
        tk.Label(
            frame, text=f" {accion}",
            bg=PANEL, fg=TEXT_SOFT, font=self.f_tip
        ).pack(side="left")

    def _borde_entrada(self, parent):
        """Marco decorativo bajo la entrada."""
        borde = tk.Frame(parent, bg=ACCENT, height=1)
        borde.place(relx=0, rely=1.0, relwidth=0.78, anchor="sw")

    @staticmethod
    def _oscurecer(hex_color: str, factor: float = 0.8) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return "#{:02X}{:02X}{:02X}".format(
            int(r * factor), int(g * factor), int(b * factor)
        )

    # ─────────────── placeholder ─────────────────────────────────────────────
    def _clear_placeholder(self, _event=None):
        if self.entrada.get() == "Escribe una nueva tarea...":
            self.entrada.delete(0, "end")
            self.entrada.config(fg=TEXT)

    def _restore_placeholder(self, _event=None):
        if not self.entrada.get().strip():
            self.entrada.insert(0, "Escribe una nueva tarea...")
            self.entrada.config(fg=TEXT_SOFT)

    # ─────────────── hover lista ──────────────────────────────────────────────
    def _hover_lista(self, event):
        idx = self.lista.nearest(event.y)
        if 0 <= idx < len(self.tareas):
            if idx not in self.lista.curselection():
                self.lista.itemconfig(idx, bg=HOVER)
        # restaurar los que no son hover ni selección
        for i in range(len(self.tareas)):
            if i != idx and i not in self.lista.curselection():
                bg = DONE_BG if self.tareas[i]["completada"] else CARD
                self.lista.itemconfig(i, bg=bg)

    def _reset_hover(self):
        for i in range(len(self.tareas)):
            if i not in self.lista.curselection():
                bg = DONE_BG if self.tareas[i]["completada"] else CARD
                self.lista.itemconfig(i, bg=bg)

    # ─────────────── atajos de teclado ────────────────────────────────────────
    def _atajos(self):
        self.root.bind("<Return>",  lambda e: self.añadir_tarea())
        self.root.bind("<c>",       lambda e: self.completar_tarea())
        self.root.bind("<C>",       lambda e: self.completar_tarea())
        self.root.bind("<Delete>",  lambda e: self.eliminar_tarea())
        self.root.bind("<d>",       lambda e: self.eliminar_tarea())
        self.root.bind("<D>",       lambda e: self.eliminar_tarea())
        self.root.bind("<Escape>",  lambda e: self._salir())

    # ─────────────── lógica de tareas ────────────────────────────────────────
    def añadir_tarea(self):
        texto = self.entrada.get().strip()
        if not texto or texto == "Escribe una nueva tarea...":
            self._shake_entrada()
            return

        self.tareas.append({"texto": texto, "completada": False})
        self._refrescar_lista()

        self.entrada.delete(0, "end")
        self.entrada.config(fg=TEXT)
        self._actualizar_contador()

    def completar_tarea(self):
        sel = self.lista.curselection()
        if not sel:
            return
        idx = sel[0]
        self.tareas[idx]["completada"] = not self.tareas[idx]["completada"]
        self._refrescar_lista()
        # mantener selección
        self.lista.selection_set(idx)
        self._actualizar_contador()

    def eliminar_tarea(self):
        sel = self.lista.curselection()
        if not sel:
            return
        idx = sel[0]
        del self.tareas[idx]
        self._refrescar_lista()
        # seleccionar el siguiente si existe
        if self.tareas:
            nuevo_idx = min(idx, len(self.tareas) - 1)
            self.lista.selection_set(nuevo_idx)
        self._actualizar_contador()

    def limpiar_completadas(self):
        antes = len(self.tareas)
        self.tareas = [t for t in self.tareas if not t["completada"]]
        if len(self.tareas) == antes:
            return
        self._refrescar_lista()
        self._actualizar_contador()

    # ─────────────── helpers internos ────────────────────────────────────────
    def _refrescar_lista(self):
        self.lista.delete(0, "end")
        for tarea in self.tareas:
            prefijo = "✔  " if tarea["completada"] else "○  "
            self.lista.insert("end", f"  {prefijo}{tarea['texto']}")

        # Aplicar colores de estado
        for i, tarea in enumerate(self.tareas):
            if tarea["completada"]:
                self.lista.itemconfig(
                    i, fg=DONE_FG, bg=DONE_BG,
                    selectforeground=DONE_FG
                )
            else:
                self.lista.itemconfig(
                    i, fg=TEXT, bg=CARD,
                    selectforeground=TEXT
                )

    def _actualizar_contador(self):
        total     = len(self.tareas)
        pendientes = sum(1 for t in self.tareas if not t["completada"])
        completadas = total - pendientes
        self.lbl_contador.config(
            text=f"{total} tarea{'s' if total != 1 else ''}  ·  "
                 f"{pendientes} pendiente{'s' if pendientes != 1 else ''}  ·  "
                 f"{completadas} completada{'s' if completadas != 1 else ''}"
        )

    def _shake_entrada(self):
        """Animación de sacudida cuando la entrada está vacía."""
        x_orig = self.entrada.winfo_x()
        offsets = [6, -6, 4, -4, 2, -2, 0]

        def _paso(i=0):
            if i < len(offsets):
                self.entrada.place_forget()
                self.entrada.pack_configure(padx=(offsets[i], 0))
                self.root.after(40, lambda: _paso(i + 1))

        self.entrada.config(bg="#3A1A2A")
        self.root.after(300, lambda: self.entrada.config(bg=CARD))

    def _salir(self):
        if messagebox.askokcancel(
            "Salir",
            "¿Deseas cerrar el Gestor de Tareas?",
            parent=self.root
        ):
            self.root.destroy()


# ─────────────────────────── MAIN ────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)

    # Centrar ventana en pantalla
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    root.mainloop()