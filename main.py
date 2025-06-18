import tkinter as tk
from tkinter import ttk, messagebox

# Simulador temporal de usuarios (se reemplazará por base de datos)
usuarios_registrados = {
    "admin": "1234"
}

class LoginVentana:
    def __init__(self, master):
        self.master = master
        self.master.title("Inicio de Sesión")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self.master, text="Sistema de Cálculos Eléctricos", font=("Segoe UI", 14, "bold")).pack(pady=20)

        frame = ttk.Frame(self.master)
        frame.pack(pady=10)

        ttk.Label(frame, text="Usuario:").grid(row=0, column=0, pady=5, sticky="e")
        self.usuario_entry = ttk.Entry(frame)
        self.usuario_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, pady=5, sticky="e")
        self.clave_entry = ttk.Entry(frame, show="*")
        self.clave_entry.grid(row=1, column=1, pady=5)

        ttk.Button(self.master, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=10)
        ttk.Button(self.master, text="Registrarse", command=self.abrir_registro).pack()

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        clave = self.clave_entry.get()

        if usuario in usuarios_registrados and usuarios_registrados[usuario] == clave:
            messagebox.showinfo("Acceso concedido", f"Bienvenido {usuario}")
            self.master.destroy()
            from menuprincipal import MenuPrincipal
            root = tk.Tk()
            MenuPrincipal(root)
            root.mainloop()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        RegistroVentana()

class RegistroVentana:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Registro de Usuario")
        self.ventana.geometry("350x200")
        self.ventana.resizable(False, False)

        ttk.Label(self.ventana, text="Nombre de usuario:").pack(pady=5)
        self.usuario_nuevo = ttk.Entry(self.ventana)
        self.usuario_nuevo.pack()

        ttk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.clave_nueva = ttk.Entry(self.ventana, show="*")
        self.clave_nueva.pack()

        ttk.Button(self.ventana, text="Registrar", command=self.registrar_usuario).pack(pady=10)

    def registrar_usuario(self):
        user = self.usuario_nuevo.get()
        pwd = self.clave_nueva.get()
        if user and pwd:
            if user in usuarios_registrados:
                messagebox.showerror("Error", "El usuario ya existe.")
            else:
                usuarios_registrados[user] = pwd
                messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
                self.ventana.destroy()
        else:
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginVentana(root)
    root.mainloop()
