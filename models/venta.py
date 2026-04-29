from database.conexion import obtener_conexion


class Venta:

    # =========================
    # REGISTRAR VENTA SIMPLE
    # =========================
    @staticmethod
    def registrar(total, utilidad):
        db = obtener_conexion()

        db.execute(
            'INSERT INTO ventas (total, utilidad) VALUES (?, ?)',
            (total, utilidad)
        )

        db.commit()
        db.close()


    # =========================
    # REGISTRAR VENTA DESDE CARRITO (PUNTO DE VENTA)
    # =========================
    @staticmethod
    def registrar_transaccion(carrito):
        db = obtener_conexion()

        total = 0
        utilidad = 0

        for item in carrito:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal

            # utilidad estimada (puedes mejorar luego con costo real)
            utilidad += subtotal * 0.3

            # 🔥 DESCARGA DE INVENTARIO
            db.execute(
                "UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?",
                (item['cantidad'], item['codigo_barras'])
            )

        # 🔥 GUARDAR VENTA
        db.execute(
            'INSERT INTO ventas (total, utilidad) VALUES (?, ?)',
            (total, utilidad)
        )

        db.commit()
        db.close()

        return total


    # =========================
    # RESUMEN DEL DÍA (DASHBOARD)
    # =========================
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

        return {
            "total": 0,
            "utilidad": 0
        }


    # =========================
    # VENTAS RECIENTES (INDEX)
    # =========================
    @staticmethod
    def obtener_recientes(limit=10):
        db = obtener_conexion()

        rows = db.execute('''
            SELECT id, fecha, total, utilidad
            FROM ventas
            ORDER BY fecha DESC
            LIMIT ?
        ''', (limit,)).fetchall()

        db.close()

        # 🔥 FIX CRÍTICO: convertir sqlite Row a dict
        return [dict(row) for row in rows]