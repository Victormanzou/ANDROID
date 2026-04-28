from database.conexion import obtener_conexion

class Merma:
    @staticmethod
    def registrar(codigo_barras, cantidad, motivo):
        db = obtener_conexion()
        # 1. Restar del stock
        db.execute('UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?', (cantidad, codigo_barras))
        # 2. Podrías tener una tabla 'mermas' en tu SQL, si no, lo guardamos en finanzas como pérdida
        db.execute('INSERT INTO finanzas (concepto, monto, tipo) VALUES (?, ?, ?)', 
                   (f"MERMA: {codigo_barras} - {motivo}", 0, 'Merma'))
        db.commit()
        db.close()