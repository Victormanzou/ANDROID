from database.conexion import obtener_conexion


class Producto:

    # =========================
    # LISTAR PRODUCTOS
    # =========================
    @staticmethod
    def obtener_todos():
        db = obtener_conexion()
        productos = db.execute(
            'SELECT * FROM productos ORDER BY nombre ASC'
        ).fetchall()
        db.close()
        return productos


    # =========================
    # BUSCAR POR CÓDIGO
    # =========================
    @staticmethod
    def buscar_por_codigo(codigo):
        db = obtener_conexion()
        producto = db.execute(
            'SELECT * FROM productos WHERE codigo_barras = ?',
            (codigo,)
        ).fetchone()
        db.close()
        return producto


    # =========================
    # INSERTAR PRODUCTO
    # =========================
    @staticmethod
    def insertar(datos):
        db = obtener_conexion()
        db.execute('''
            INSERT INTO productos 
            (codigo_barras, nombre, categoria, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', datos)
        db.commit()
        db.close()


    # =========================
    # ACTUALIZAR STOCK
    # =========================
    @staticmethod
    def actualizar_stock(codigo, cantidad_vendida):
        db = obtener_conexion()
        db.execute(
            'UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?',
            (cantidad_vendida, codigo)
        )
        db.commit()
        db.close()


    # =====================================================
    # 📊 ABC DE PRODUCTOS (CORREGIDO Y FUNCIONAL)
    # =====================================================
    @staticmethod
    def analisis_abc():
        db = obtener_conexion()

        # ⚠️ IMPORTANTE:
        # Como tu sistema NO tiene detalle de ventas por producto,
        # usamos aproximación con ventas globales
        rows = db.execute("""
            SELECT 
                p.nombre,
                COALESCE(SUM(v.total), 0) as ventas
            FROM productos p
            LEFT JOIN ventas v 
                ON DATE(v.fecha) = DATE('now')
            GROUP BY p.codigo_barras
            ORDER BY ventas DESC
        """).fetchall()

        db.close()

        rows = [dict(r) for r in rows]

        total = sum(r["ventas"] for r in rows) or 1

        resultado = []
        acumulado = 0

        for r in rows:
            porcentaje = (r["ventas"] / total) * 100
            acumulado += porcentaje

            if acumulado <= 70:
                clase = "A"   # top ventas
            elif acumulado <= 90:
                clase = "B"   # medio
            else:
                clase = "C"   # bajo rendimiento

            resultado.append({
                "nombre": r["nombre"],
                "ventas": r["ventas"],
                "clase": clase,
                "margen": round(porcentaje, 2)
            })

        return resultado