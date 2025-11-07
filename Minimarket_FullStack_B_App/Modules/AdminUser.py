import tkinter as tk
from tkinter import ttk, messagebox
from Database.db_connection import conectar


class AdminUserApp:
    def __init__(self, root, es_super_user=False):
        self.root = root
        self.es_super_user = es_super_user
        self.root.title("Administrar Usuarios")

        # Frame superior: formulario
        frame_form = tk.Frame(root)
        frame_form.pack(pady=10, fill="x", padx=20)

        # Campos
        campos = ["Nombre", "Email", "Rol"]
        self.entries = {}

        for i, campo in enumerate(campos):
            tk.Label(frame_form, text=campo + ":").grid(
                row=i, column=0, sticky="w", pady=2
            )
            if campo in ["Rol"]:
                self.entries[campo] = ttk.Combobox(frame_form, width=30, values=[
                                                   "admin", "empleado", "super_usuario"], state="readonly")
            else:
                self.entries[campo] = tk.Entry(frame_form, width=33)
            self.entries[campo].grid(row=i, column=1, pady=2, padx=5)

        # Botones
        if not self.es_super_user:
            tk.Button(btn_frame, text="Agregar", state="disabled",
                      bg="gray").pack(side="left", padx=5)
            tk.Button(btn_frame, text="Actualizar", state="disabled",
                      bg="gray").pack(side="left", padx=5)
            tk.Button(btn_frame, text="Eliminar", state="disabled",
                      bg="gray").pack(side="left", padx=5)
        else:
            btn_frame = tk.Frame(frame_form)
            btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

            tk.Button(btn_frame, text="Agregar", bg="#4CAF50", fg="green",
                      command=self.agregar).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Actualizar", bg="#2196F3", fg="blue",
                      command=self.actualizar).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Eliminar", bg="#F44336", fg="red",
                      command=self.eliminar).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Limpiar",
                      command=self.limpiar).pack(side="left", padx=5)

        # Tabla
        self.tree = ttk.Treeview(
            root,
            columns=("ID", "Nombre", "Email", "Rol"),
            show="headings",
            height=15
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Cargar datos
        self.cargar_usuarios()
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM usuarios
            """)

            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()

    def agregar(self):
        datos = self.obtener_datos()
        if not datos:
            return

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, rol)
                VALUES (%s, %s, %s)
            """, (*datos,))  # ← Usa *datos y coma final

            conn.commit()
            conn.close()
            self.cargar_usuarios()
            self.limpiar()
            messagebox.showinfo("Éxito", "Usuario agregado")

    def actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un usuario")
            return

        item = self.tree.item(seleccion[0])
        usuario_id = item["values"][0]
        datos = self.obtener_datos()
        if not datos:
            return

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuarios SET nombre=%s, email=%s, rol=%s
                WHERE id=%s
            """, (*datos, usuario_id))

            conn.commit()
            conn.close()
            self.cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario actualizado")

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un usuario")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar usuario?"):
            usuario_id = self.tree.item(seleccion[0])["values"][0]

            conn = conectar()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM usuarios WHERE id=%s", (usuario_id,)
                )
                conn.commit()
                conn.close()
                self.cargar_usuarios()

    def seleccionar(self, event):
        seleccion = self.tree.selection()

        if seleccion:
            valores = self.tree.item(seleccion[0])["values"]
            self.limpiar()

            self.entries["Nombre"].insert(0, valores[1])
            self.entries["Email"].insert(0, valores[2])
            self.entries["Rol"].insert(0, valores[3])

    def obtener_datos(self):
        nombre = self.entries["Nombre"].get().strip()
        email = self.entries["Email"].get().strip()
        rol = self.entries["Rol"].get().strip()

        if not all([nombre, email, rol]):
            messagebox.showwarning("Faltan datos", "Completa todos los campos")
            return None
        return (nombre, email, rol)

    def limpiar(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, "end")
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
