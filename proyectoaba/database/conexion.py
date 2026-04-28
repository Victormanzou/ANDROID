import sqlite3
import os

def obtener_conexion():
    # Esto asegura que busque 'abarrotes.db' dentro de la carpeta 'database'
    base_dir = os.path.dirname(__file__)
    ruta_db = os.path.join(base_dir, 'abarrotes.db')
    
    conexion = sqlite3.connect(ruta_db)
    conexion.row_factory = sqlite3.Row
    return conexion