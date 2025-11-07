# modules/login.py
import tkinter as tk
from tkinter import ttk, messagebox
from Database.db_connection import conectar
from Modules.Menu import MenuApp


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimarket - Login")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        tk.Label(root, text="INICIAR SESIÓN", font=(
            "Arial", 16, "bold")).pack(pady=15)

        tk.Label(root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "Fabricio@minimarket.com")

        tk.Label(root, text="Rol:").pack(pady=5)
        self.rol_var = tk.StringVar(value="super_usuario")
        ttk.Combobox(root, textvariable=self.rol_var, values=[
                     "admin", "empleado", "super_usuario"], state="readonly", width=27).pack(pady=5)

        tk.Button(root, text="INGRESAR", bg="#B1451C", fg="black", font=(
            "Arial", 10, "bold"), command=self.login).pack(pady=15)

    def login(self):
        email = self.email_entry.get().strip()
        rol = self.rol_var.get()

        if not email or not rol:
            messagebox.showwarning("Datos incompletos",
                                   "Completa todos los campos")
            return

        conn = conectar()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, email, rol FROM usuarios WHERE email = %s AND rol = %s", (email, rol))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                messagebox.showinfo("Exito", f"Bienvenido {usuario[1]}")
                self.root.destroy()
                root_menu = tk.Tk()
                MenuApp(root_menu, usuario)
                root_menu.mainloop()
            else:
                messagebox.showerror("Error", "Email o rol incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Error en login: {e}")
