from database.conexion import obtener_conexion
from datetime import datetime

class Venta:

    @staticmethod
    def registrar(total, utilidad):
        db = obtener_conexion()
        db.execute(
            'INSERT INTO ventas (total, utilidad) VALUES (?, ?)',
            (total, utilidad)
        )
        db.commit()
        db.close()

    # 🔥 NUEVO: registrar venta desde carrito
    @staticmethod
    def registrar_transaccion(carrito):
        db = obtener_conexion()

        total = 0
        utilidad = 0

        for item in carrito:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal

            # utilidad simple (puedes mejorarla después)
            utilidad += subtotal * 0.3  # ejemplo 30%

        db.execute(
            'INSERT INTO ventas (total, utilidad) VALUES (?, ?)',
            (total, utilidad)
        )

        db.commit()
        db.close()

        return total

    @staticmethod
    def obtener_resumen_hoy():
        db = obtener_conexion()

        resumen = db.execute('''
            SELECT 
                SUM(total) as total,
                SUM(utilidad) as utilidad 
            FROM ventas 
            WHERE DATE(fecha) = DATE('now')
        ''').fetchone()

        db.close()

        if resumen:
            return {
                "total": resumen["total"] or 0,
                "utilidad": resumen["utilidad"] or 0
            }

        return {"total": 0, "utilidad": 0}

    # 🔥 NUEVO: para dashboard (últimas ventas)
    @staticmethod
    def obtener_recientes(limit=10):
        db = obtener_conexion()

        rows = db.execute('''
            SELECT * FROM ventas
            ORDER BY fecha DESC
            LIMIT ?
        ''', (limit,)).fetchall()

        db.close()
        return rows