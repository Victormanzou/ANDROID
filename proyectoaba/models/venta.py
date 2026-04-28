from database.conexion import obtener_conexion

class Venta:
    @staticmethod
    def registrar(total, utilidad):
        db = obtener_conexion()
        db.execute('INSERT INTO ventas (total, utilidad) VALUES (?, ?)', (total, utilidad))
        db.commit()
        db.close()

    @staticmethod
    def obtener_resumen_hoy():
        db = obtener_conexion()
        # Trae la suma de ventas y utilidades del día actual
        resumen = db.execute('''SELECT SUM(total) as total, SUM(utilidad) as utilidad 
                                FROM ventas 
                                WHERE DATE(fecha) = DATE('now')''').fetchone()
        db.close()
        return resumen