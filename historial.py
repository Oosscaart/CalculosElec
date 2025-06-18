import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from exportador import exportar_resultado_pdf

# Simulador de datos
datos_simulados = [
    {"proyecto": "Carga Motor 1", "usuario": "admin", "fecha": "2024-05-12", "voltaje": "440V", "interruptor": "100A", "calibre": "3/0"},
    {"proyecto": "Transformador A", "usuario": "admin", "fecha": "2024-05-11", "voltaje": "220V", "interruptor": "60A", "calibre": "2/0"},
    {"proyecto": "Panel Oficina", "usuario": "ariadna", "fecha": "2024-05-10", "voltaje": "127V", "interruptor": "40A", "calibre": "6 AWG"},
]

class HistorialVentana:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Historial de Proyectos")
        self.ventana.geometry("700x400")
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self.ventana, text="Cargas Guardadas", font=("Segoe UI", 14, "bold")).pack(pady=10)

        columnas = ("proyecto", "usuario", "fecha", "voltaje", "interruptor", "calibre")

        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=100, anchor="center")
        self.tabla.pack(pady=10)

        for row in datos_simulados:
            self.tabla.insert("", "end", values=(
                row["proyecto"], row["usuario"], row["fecha"], row["voltaje"], row["interruptor"], row["calibre"]
            ))

        # Botones
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Ver Detalles", command=self.ver_detalles).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Exportar a PDF", command=self.exportar_pdf).pack(side="left", padx=10)

    def ver_detalles(self):
        seleccionado = self.tabla.selection()
        if seleccionado:
            valores = self.tabla.item(seleccionado)["values"]
            messagebox.showinfo("Detalles del Proyecto", f"Proyecto: {valores[0]}\nUsuario: {valores[1]}\nFecha: {valores[2]}")
        else:
            messagebox.showwarning("Selecciona una fila", "Por favor selecciona un proyecto.")

    def exportar_pdf(self):
        seleccionado = self.tabla.selection()
        if seleccionado:
            valores = self.tabla.item(seleccionado)["values"]

            datos_proyecto = {
                "proyecto": valores[0],
                "usuario": valores[1],
                "fecha": valores[2],
                "voltaje": valores[3],
                "interruptor": valores[4],
                "calibre": valores[5],
            }

            # Explorar archivos para guardar
            ruta_pdf = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                initialfile=f"{valores[0]}_calculo.pdf",
                title="Guardar PDF como..."
            )

            if ruta_pdf:
                try:
                    exportar_resultado_pdf(
                        resultados=datos_proyecto,
                        nombre_archivo=ruta_pdf,
                        usuario=valores[1],
                        proyecto=valores[0]
                    )
                    messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\n{ruta_pdf}")
                except Exception as e:
                    messagebox.showerror("Error al exportar", str(e))
        else:
            messagebox.showwarning("Selecciona un proyecto", "Por favor selecciona un proyecto para exportar.")
