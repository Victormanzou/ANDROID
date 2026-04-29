from database.conexion import obtener_conexion

class Compra:

    @staticmethod
    def registrar_entrada(codigo_barras, cantidad, costo_unitario):
        db = obtener_conexion()

        try:
            # 🔍 1. Verificar que el producto exista
            producto = db.execute(
                "SELECT stock FROM productos WHERE codigo_barras = ?",
                (codigo_barras,)
            ).fetchone()

            if not producto:
                db.close()
                raise Exception("Producto no encontrado")

            total = cantidad * costo_unitario

            # 📦 2. Aumentar stock
            db.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE codigo_barras = ?
            """, (cantidad, codigo_barras))

            # 🧾 3. Registrar compra (HISTORIAL REAL)
            db.execute("""
                INSERT INTO compras (codigo_barras, cantidad, costo_unitario, total)
                VALUES (?, ?, ?, ?)
            """, (codigo_barras, cantidad, costo_unitario, total))

            # 💸 4. Registrar en finanzas
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