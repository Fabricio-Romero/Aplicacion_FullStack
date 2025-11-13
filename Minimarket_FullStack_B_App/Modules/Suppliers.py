import tkinter as tk
from tkinter import ttk, messagebox
from turtle import st
from typing import Self
from Database.db_connection import conectar
from datetime import datetime


class ProveedoresApp:
    def __init__(self, root, es_admin=False):
        self.root = root
        self.es_admin = es_admin
        self.root.title("Proveedores")

        frame = tk.Frame(root)
        frame.pack(pady=15, padx=20)

        self.entries = {}

        tk.Label(frame, text="Nombre:").grid(
            row=0, column=0, sticky="w", pady=2)
        self.entries["Nombre"] = tk.Entry(frame, width=25)
        self.entries["Nombre"].grid(
            row=0, column=1, pady=2, padx=5)

        tk.Label(frame, text="Contacto:").grid(
            row=0, column=2, sticky="w", pady=2)
        self.entries["Contacto"] = tk.Entry(frame, width=25)
        self.entries["Contacto"].grid(
            row=0, column=3, pady=2, padx=5)

        tk.Label(frame, text="Teléfono:").grid(
            row=0, column=4, sticky="w", pady=2)
        self.entries["Telefono"] = tk.Entry(frame, width=25)
        self.entries["Telefono"].grid(
            row=0, column=5, pady=2, padx=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=2, padx=2)

        tk.Button(
            button_frame, text="AGREGAR", bg="#6CFF22", fg="blue",
            font=("Arial", 10, "bold"),
            command=self.agregar
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            button_frame, text="ACTUALIZAR", bg="#227EFF", fg="orange",
            font=("Arial", 10, "bold"),
            command=self.actualizar
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            button_frame, text="ELIMINAR", bg="#F80000", fg="black",
            font=("Arial", 10, "bold"),
            command=self.eliminar
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            button_frame, text="LIMPIAR", bg="#00F2FF", fg="green",
            font=("Arial", 10, "bold"),
            command=self.limpiar
        ).grid(row=0, column=3, padx=5)

        # Tabla de proveedores
        self.tree = ttk.Treeview(
            root,
            columns=("id", "nombre", "contacto", "telefono"),
            show="headings",
            height=15
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column("id", width=3, anchor="center")
            self.tree.column("nombre", width=125, anchor="center")
            self.tree.column("contacto", width=125, anchor="center")
            self.tree.column("telefono", width=125, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        self.cargar_proveedores()
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    def agregar(self):
        datos = self.obtener_datos()
        if not datos:
            return

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proveedores (nombre, contacto, telefono)
                VALUES (%s, %s, %s)
            """, (*datos,))  # ← Usa *datos y coma final

            conn.commit()
            conn.close()
            self.cargar_proveedores()
            self.limpiar()
            messagebox.showinfo("Éxito", "Proveedor agregado")

    def actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un proveedor")
            return

        item = self.tree.item(seleccion[0])
        proveedor_id = item["values"][0]
        datos = self.obtener_datos()
        if not datos:
            return

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s
                WHERE id=%s
            """, (*datos, proveedor_id))

            conn.commit()
            conn.close()
            self.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor actualizado")

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un proveedor")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar proveedor?"):
            proveedor_id = self.tree.item(seleccion[0])["values"][0]

            conn = conectar()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM proveedores WHERE id=%s", (proveedor_id,)
                )
                conn.commit()
                conn.close()
                self.cargar_proveedores()

    def limpiar(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, "end")
            elif isinstance(entry, ttk.Combobox):
                entry.set("")

    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM proveedores
            """)

            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()

    def seleccionar(self, event):
        seleccion = self.tree.selection()

        if seleccion:
            valores = self.tree.item(seleccion[0])["values"]
            self.limpiar()

            self.entries["Nombre"].insert(0, valores[1])
            self.entries["Contacto"].insert(0, valores[2])
            self.entries["Telefono"].insert(0, valores[3])

    def obtener_datos(self):
        nombre = self.entries["Nombre"].get().strip()
        contacto = self.entries["Contacto"].get().strip()
        telefono = self.entries["Telefono"].get().strip()
        return nombre, contacto, telefono
