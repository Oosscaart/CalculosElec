import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Cálculos Eléctricos - NOM-001-SEDE-2012")
        self.master.geometry("700x500")
        self.master.resizable(False, False)

        # Fondo
        self.fondo_path = "fondo.jpg"  # Asegúrate de tener este archivo
        self.imagen_fondo = Image.open(self.fondo_path).resize((700, 500), Image.Resampling.LANCZOS)
        self.fondo = ImageTk.PhotoImage(self.imagen_fondo)

        # Canvas
        self.canvas = tk.Canvas(self.master, width=700, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")

        # Frame para botones
        self.frame = tk.Frame(self.master, bg="", bd=0)
        self.canvas.create_window(350, 250, window=self.frame)

        self._crear_widgets()

    def _crear_widgets(self):
        # Encabezado
        tk.Label(self.frame, text="Sistema de Cálculos Eléctricos", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=(10, 5))
        tk.Label(self.frame, text="Conforme a NOM-001-SEDE-2012", font=("Segoe UI", 11)).grid(row=1, column=0)

        # Botones
        botones = [
            ("Cálculos Eléctricos", self.abrir_calculos),
            ("Historial de Cargas", self.abrir_historial),
            ("Acerca del sistema", self.abrir_acerca),
            ("Salir", self.master.quit),
        ]

        for i, (texto, comando) in enumerate(botones):
            tk.Button(self.frame, text=texto, command=comando, width=30).grid(row=2 + i, column=0, pady=8)

    def abrir_calculos(self):
        from Modulos import VentanaCalculos
        VentanaCalculos(self.master)

    def abrir_acerca(self):
        messagebox.showinfo("Acerca del sistema", "Sistema desarrollado por Ariadna Aguilar\nResidencia Profesional 2025\nBasado en NOM-001-SEDE-2012")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
