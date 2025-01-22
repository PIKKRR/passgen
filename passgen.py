import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os
from datetime import datetime

SIMBOLOS_PERMITIDOS = "¡!¿?=-_çÇ+.,$%&/()"

def generar_contraseña():
    try:
        
        longitud = int(entry_longitud.get())
        if longitud <= 0:
            raise ValueError
        
        usar_mayusculas = var_mayus.get()
        usar_minusculas = var_minus.get()
        usar_numeros = var_num.get()
        usar_simbolos = var_sym.get()
        
        if not (usar_mayusculas or usar_minusculas or usar_numeros or usar_simbolos):
            messagebox.showerror("Error", "Debes seleccionar al menos un tipo de carácter.")
            return
        
        caracteres_disponibles = ""
        if usar_mayusculas:
            caracteres_disponibles += string.ascii_uppercase
        if usar_minusculas:
            caracteres_disponibles += string.ascii_lowercase
        if usar_numeros:
            caracteres_disponibles += string.digits
        if usar_simbolos:

            caracteres_disponibles += SIMBOLOS_PERMITIDOS
        
        caracteres_obligatorios = []
        if usar_mayusculas:
            caracteres_obligatorios.append(random.choice(string.ascii_uppercase))
        if usar_minusculas:
            caracteres_obligatorios.append(random.choice(string.ascii_lowercase))
        if usar_numeros:
            caracteres_obligatorios.append(random.choice(string.digits))
        if usar_simbolos:
            caracteres_obligatorios.append(random.choice(SIMBOLOS_PERMITIDOS))
        
        if longitud < len(caracteres_obligatorios):
            messagebox.showerror("Error", 
                                 f"La longitud mínima debe ser de al menos {len(caracteres_obligatorios)} "
                                 "para incluir al menos uno de cada tipo seleccionado.")
            return
        
        restante = longitud - len(caracteres_obligatorios)
        lista_contraseña = caracteres_obligatorios + [random.choice(caracteres_disponibles) for _ in range(restante)]
        
        random.shuffle(lista_contraseña)
        
        contraseña = ''.join(lista_contraseña)
        
        label_resultado.config(text=contraseña, fg="blue")
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número válido para la longitud.")

def copiar_contraseña():

    password_text = label_resultado.cget("text")

    if password_text and password_text != "Tu contraseña se mostrará aquí":
        ventana.clipboard_clear()
        ventana.clipboard_append(password_text)
        ventana.update()
        messagebox.showinfo("Copiar contraseña", "¡Contraseña copiada al portapapeles!")
    else:
        messagebox.showwarning("Copiar contraseña", "No hay ninguna contraseña generada para copiar.")

def guardar_en_log():

    password_text = label_resultado.cget("text")
    if not password_text or password_text == "Tu contraseña se mostrará aquí":
        messagebox.showwarning("Guardar en log", "Primero genera una contraseña para poder guardarla.")
        return
    
    destino_text = entry_destino.get().strip()[:50]
    if not destino_text:
        messagebox.showwarning("Guardar en log", "Por favor, escribe un destino antes de guardar.")
        return
    
    registro = {
        "Destino": destino_text,
        "Contraseña guardada": password_text,
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    log_filename = "log.json"
    
    if os.path.exists(log_filename):
        try:
            with open(log_filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = []
    else:
        data = []
    
    data.append(registro)
    
    with open(log_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    messagebox.showinfo("Guardar en log", "¡La contraseña se ha guardado correctamente en el log!")

ventana = tk.Tk()
ventana.title("Generador de Contraseñas")
ventana.geometry("420x400")

frame = tk.Frame(ventana)
frame.pack(pady=10)

label_longitud = tk.Label(frame, text="Longitud de la contraseña:")
label_longitud.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_longitud = tk.Entry(frame, width=5)
entry_longitud.grid(row=0, column=1, padx=5, pady=5)
entry_longitud.insert(0, "8")

var_mayus = tk.BooleanVar(value=True)
var_minus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_sym = tk.BooleanVar(value=True)

check_mayus = tk.Checkbutton(frame, text="Mayúsculas", variable=var_mayus)
check_minus = tk.Checkbutton(frame, text="Minúsculas", variable=var_minus)
check_num = tk.Checkbutton(frame, text="Números",    variable=var_num)
check_sym = tk.Checkbutton(frame, text="Símbolos",   variable=var_sym)

check_mayus.grid(row=1, column=0, padx=5, pady=5, sticky="w")
check_minus.grid(row=1, column=1, padx=5, pady=5, sticky="w")
check_num.grid(row=2, column=0, padx=5, pady=5, sticky="w")
check_sym.grid(row=2, column=1, padx=5, pady=5, sticky="w")

boton_generar = tk.Button(frame, text="Generar contraseña", command=generar_contraseña)
boton_generar.grid(row=3, column=0, columnspan=2, pady=10)

label_resultado = tk.Label(frame, text="Tu contraseña se mostrará aquí", fg="gray")
label_resultado.grid(row=4, column=0, columnspan=2, pady=10)

boton_copiar = tk.Button(frame, text="Copiar contraseña", command=copiar_contraseña)
boton_copiar.grid(row=5, column=0, columnspan=2, pady=10)

frame_destino = tk.Frame(frame)
frame_destino.grid(row=6, column=0, columnspan=2, pady=5)

label_destino = tk.Label(frame_destino, text="Destino:")
label_destino.pack(side="left", padx=5)

entry_destino = tk.Entry(frame_destino, width=30)
entry_destino.pack(side="left", padx=5)

boton_guardar = tk.Button(frame, text="Guardar en log", command=guardar_en_log)
boton_guardar.grid(row=7, column=0, columnspan=2, pady=10)

footer_label = tk.Label(ventana, text="Programa creado por PIKKRR", fg="gray")
footer_label.pack(side="bottom", pady=5)

ventana.mainloop()