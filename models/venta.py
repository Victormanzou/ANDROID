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
    # VENTA DESDE CARRITO (POS)
    # =========================
    @staticmethod
    def registrar_transaccion(carrito):
        db = obtener_conexion()

        total = 0
        utilidad = 0

        for item in carrito:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal

            utilidad += subtotal * 0.3

            # descontar stock
            db.execute(
                "UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?",
                (item['cantidad'], item['codigo_barras'])
            )

        db.execute(
            'INSERT INTO ventas (total, utilidad) VALUES (?, ?)',
            (total, utilidad)
        )

        db.commit()
        db.close()

        return total


    # =========================
    # RESUMEN HOY
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

        return {
            "total": resumen["total"] or 0,
            "utilidad": resumen["utilidad"] or 0
        } if resumen else {"total": 0, "utilidad": 0}


    # =========================
    # VENTAS RECIENTES
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

        return [dict(row) for row in rows]


    # =========================
    # 📊 VENTAS SEMANALES (GRÁFICA)
    # =========================
    @staticmethod
    def obtener_resumen_semanal():
        db = obtener_conexion()

        rows = db.execute("""
            SELECT 
                strftime('%w', fecha) as dia,
                SUM(total) as total
            FROM ventas
            WHERE DATE(fecha) >= DATE('now','-7 day')
            GROUP BY dia
        """).fetchall()

        db.close()

        datos = [0] * 7  # domingo = 0 ... sábado = 6

        for r in rows:
            datos[int(r["dia"])] = r["total"] or 0

        return datos


    # =========================
    # 📊 ABC DE PRODUCTOS
    # =========================
    @staticmethod
    def obtener_abc():
        db = obtener_conexion()

        rows = db.execute("""
            SELECT 
                nombre,
                SUM(total) as ventas
            FROM ventas
            GROUP BY nombre
            ORDER BY ventas DESC
        """).fetchall()

        db.close()

        total = sum(r["ventas"] for r in rows) if rows else 0

        resultado = []
        acumulado = 0

        for r in rows:
            acumulado += r["ventas"]

            porcentaje = (acumulado / total) * 100 if total else 0

            if porcentaje <= 70:
                clase = "A"   # top ventas
            elif porcentaje <= 90:
                clase = "B"   # medio
            else:
                clase = "C"   # bajo rendimiento

            resultado.append({
                "nombre": r["nombre"],
                "clase": clase,
                "margen": round((r["ventas"] / total) * 100, 2) if total else 0
            })

        return resultado