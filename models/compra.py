from database.conexion import obtener_conexion

class Compra:

    @staticmethod
    def registrar_entrada(codigo_barras, cantidad, costo_unitario):
        db = obtener_conexion()

        try:
            producto = db.execute(
                "SELECT stock FROM productos WHERE codigo_barras = ?",
                (codigo_barras,)
            ).fetchone()

            if not producto:
                raise Exception("Producto no encontrado")

            total = cantidad * costo_unitario

            # 📦 actualizar stock
            db.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE codigo_barras = ?
            """, (cantidad, codigo_barras))

            # 💸 finanzas
            db.execute("""
                INSERT INTO finanzas (concepto, monto, tipo)
                VALUES (?, ?, ?)
            """, (
                f"Compra de mercancía: {codigo_barras}",
                total,
                "Egreso"
            ))

            db.commit()

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()