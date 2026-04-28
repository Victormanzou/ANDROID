# models/categoria.py
from database.conexion import obtener_conexion

class Categoria:  # <--- Revisa que diga exactamente Categoria (con C mayúscula)
    @staticmethod
    def obtener_todas():
        db = obtener_conexion()
        categorias = db.execute('SELECT DISTINCT categoria FROM productos').fetchall()
        db.close()
        return categorias