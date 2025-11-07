# Archivo principal (inicia la aplicaión)

# main.py
# importamos la libreria tkinter y le ponemos el alias tk
import tkinter as tk
# se importa la funcion LoginApp desde la carpeta modules y el archivo Login
from Modules.Login import LoginApp

# ejecuta el codigo solo si el archivo se llama Main
if __name__ == "__main__":
    # crea la ventana principal de la app
    root = tk.Tk()
    # crea una instancia de la funcion LoginAp que le va a pasar el root
    app = LoginApp(root)
    # inicializa un bucle infinito para que la ventana se mantenga abierta
    root.mainloop()
