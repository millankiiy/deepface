import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from deepface import DeepFace

# ---------------------------------------------------
# FUNCIONES
# ---------------------------------------------------

def seleccionar_imagen1():
    global ruta1
    ruta1 = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.png")]
    )
    if ruta1:
        mostrar_imagen(ruta1, panel_img1)
        label_estado1.config(text="Imagen cargada", bootstyle="success")

def seleccionar_imagen2():
    global ruta2
    ruta2 = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.png")]
    )
    if ruta2:
        mostrar_imagen(ruta2, panel_img2)
        label_estado2.config(text="Imagen cargada", bootstyle="success")

def mostrar_imagen(ruta, panel):
    img = Image.open(ruta)
    img = img.resize((330, 330))
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

def comparar():
    if not ruta1 or not ruta2:
        messagebox.showerror("Error", "Debes seleccionar ambas imágenes.")
        return
    
    try:
        btn_comparar.config(text="Analizando...", bootstyle="warning")
        ventana.update_idletasks()

        resultado = DeepFace.verify(ruta1, ruta2)

        if resultado["verified"]:
            messagebox.showinfo("Resultado", "✔ Las personas coinciden.")
        else:
            messagebox.showinfo("Resultado", "✖ No coinciden.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema:\n{str(e)}")

    finally:
        btn_comparar.config(text="Comparar Rostros", bootstyle="primary")

# ---------------------------------------------------
# INTERFAZ MEJORADA
# ---------------------------------------------------

ventana = ttk.Window(
    title="Comparador Facial – DeepFace",
    themename="flatly"
)

ventana.state('zoomed')  # ⬅️ MAXIMIZADA AL ABRIR

ruta1 = None
ruta2 = None

# ⬆️ TÍTULO SUPERIOR
titulo = ttk.Label(
    ventana,
    text="Reconocimiento Facial",
    font=("Segoe UI", 28, "bold"),
    bootstyle="primary"
)
titulo.pack(pady=25)

# MARCO CONTENEDOR CENTRAL
contenedor = ttk.Frame(ventana)
contenedor.pack(pady=20)

# ----------------------------
# CARD IZQUIERDA
# ----------------------------
card1 = ttk.Labelframe(
    contenedor,
    text="Imagen 1",
    labelanchor="n",
    padding=15
)
card1.grid(row=0, column=0, padx=40)

panel_img1 = ttk.Label(card1)
panel_img1.pack()

label_estado1 = ttk.Label(card1, text="Sin imagen", bootstyle="secondary")
label_estado1.pack(pady=10)

ttk.Button(
    card1,
    text="Seleccionar Imagen 1",
    bootstyle="info-outline",
    command=seleccionar_imagen1
).pack(pady=12)

# ----------------------------
# CARD DERECHA
# ----------------------------
card2 = ttk.Labelframe(
    contenedor,
    text="Imagen 2",
    labelanchor="n",
    padding=15
)
card2.grid(row=0, column=1, padx=40)

panel_img2 = ttk.Label(card2)
panel_img2.pack()

label_estado2 = ttk.Label(card2, text="Sin imagen", bootstyle="secondary")
label_estado2.pack(pady=10)

ttk.Button(
    card2,
    text="Seleccionar Imagen 2",
    bootstyle="info-outline",
    command=seleccionar_imagen2
).pack(pady=12)

# ----------------------------
# BOTÓN PRINCIPAL
# ----------------------------
btn_comparar = ttk.Button(
    ventana,
    text="Comparar Rostros",
    bootstyle="primary",
    command=comparar,
    width=25
)
btn_comparar.pack(pady=40, ipady=10)

ventana.mainloop()
