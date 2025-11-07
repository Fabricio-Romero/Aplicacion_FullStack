# Conexión a MySQL

# database/db_connection.py
# Importa la caja de mensajes desde la libreria tkinter
from tkinter import messagebox
# Importa el modulo para conectar python con MySQL
import mysql.connector

# definimos una funcion llamada conectar


def conectar():
    """ Connecta a la base de datos MySQL """
    # intentar las siguientes lineas de codigo
    try:
        # crea una variable que va a guardar la conexion del MySQL connector
        conn = mysql.connector.connect(
            # parametros de conexion
            # el host va a ser el localhost
            host="localhost",
            # el usuario va a ser el root
            user="root",
            # la contrasenia del usuario va a ser:
            # Cambiar la contrasenia dependiendo del usuario
            password="46768032",
            # la base de datos a la que se va a conectar
            database="minimarket_fullstack_b"
        )
        # devuelve la variable conn si todo esta bien
        return conn
    # Captura errores de conexion de MySQL y los guarda en la variable e
    except mysql.connector.Error as e:
        # muestra un mensaje de error con el titulo "error de conexion" y el mensaje "no se pudo conectar a la DB"
        # hace un salto de linea y muestra la variable e
        messagebox.showerror("Error de Conexion",
                             f"No se pudo conectar a la BD:\n{e}")
        # si falla devuelve nada
        return None
