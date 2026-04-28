from database.conexion import obtener_conexion

class Compra:
    @staticmethod
    def registrar_entrada(codigo_barras, cantidad, costo_unitario):
        db = obtener_conexion()
        # 1. Aumentar el stock del producto
        db.execute('UPDATE productos SET stock = stock + ? WHERE codigo_barras = ?', (cantidad, codigo_barras))
        # 2. Registrar el egreso en finanzas (opcional)
        db.execute('INSERT INTO finanzas (concepto, monto, tipo) VALUES (?, ?, ?)', 
                   (f"Compra de mercancía: {codigo_barras}", cantidad * costo_unitario, 'Egreso'))
        db.commit()
        db.close()