import tkinter as tk
from tkinter import ttk, messagebox
from Modules.Products import ProductosApp
from Modules.Movements import MovimientosApp
from Modules.Reports import ReportesApp
from Modules.AdminUser import AdminUserApp


class MenuApp:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title(f"Minimarket - {usuario[3].title()}")
        self.root.geometry("800x600")
        tk.Label(root, text=f"Usuario: {usuario[1]} ({usuario[3]})", font=(
            "Arial", 10,)).pack(anchor="ne", padx=20, pady=10)
        tk.Label(root, text="MINIMARKET FULLSTACK B",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Definir estilo de botones grandes
        btn_style = {"width": 30, "height": 2, "font": ("Arial", 11, "bold")}
        # Botones
        tk.Button(root, text="GESTIÓN DE PRODUCTOS", bg="#2196F3", fg="white",
                  **btn_style, command=self.abrir_productos).pack(pady=10)
        tk.Button(root, text="REGISTRAR MOVIMIENTOS", bg="#FF9800", fg="white",
                  **btn_style, command=self.abrir_movimientos).pack(pady=10)
        tk.Button(root, text="VER REPORTES", bg="#9C27B0", fg="white",
                  **btn_style, command=self.abrir_reportes).pack(pady=10)
        tk.Button(root, text="ADMINISTRAR USUARIOS", bg="#40B027", fg="white",
                  **btn_style, command=self.abrir_admin_usuarios).pack(pady=10)
        tk.Button(root, text="CERRAR SESIÓN", bg="#F44336", fg="white",
                  **btn_style, command=root.destroy).pack(pady=20)

    def abrir_productos(self):
        if self.usuario[3] == "admin" or self.usuario[3] == "super_usuario":  # usuario[3] = rol
            self.nueva_ventana(
                "Productos", lambda root: ProductosApp(root, es_admin=True))
        else:
            messagebox.showwarning(
                "Acceso denegado", "Solo el admin puede gestionar productos")

    def abrir_movimientos(self):
        self.nueva_ventana("Movimientos", MovimientosApp)

    def abrir_reportes(self):
        self.nueva_ventana("Reportes", ReportesApp)

    def abrir_admin_usuarios(self):
        if self.usuario[3] == "super_usuario":
            self.nueva_ventana("AdministrarUsuarios", lambda root: AdminUserApp(
                root, es_super_user=True))
        else:
            messagebox.showwarning(
                "Acceso denegado", "Solo el super usuario puede administrar los usuarios")

    def nueva_ventana(self, titulo, clase):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("900x600")
        clase(ventana)
