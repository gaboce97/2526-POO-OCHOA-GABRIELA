# Aplicación GUI básica con Tkinter
# Permite agregar y limpiar elementos en una lista

import tkinter as tk
from tkinter import messagebox

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Mi Lista")
ventana.geometry("350x400")

# --- Etiqueta y campo de texto ---
etiqueta = tk.Label(ventana, text="Escribe tu nombre:")
etiqueta.pack(pady=10)

campo = tk.Entry(ventana, width=30)
campo.pack()

# --- Función para agregar ---
def agregar():
    texto = campo.get().strip()
    if texto == "":
        messagebox.showwarning("Aviso", "El campo está vacío.")
    else:
        lista.insert(tk.END, texto)
        campo.delete(0, tk.END)  # limpiar el campo

# --- Función para limpiar ---
def limpiar():
    lista.delete(0, tk.END)

# --- Botones ---
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar)
boton_agregar.pack(pady=5)

boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar)
boton_limpiar.pack()

# --- Lista para mostrar datos ---
lista = tk.Listbox(ventana, width=40, height=10)
lista.pack(pady=10)

# --- Iniciar la aplicación ---
ventana.mainloop()