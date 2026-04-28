from database.conexion import obtener_conexion

class Producto:
    @staticmethod
    def obtener_todos():
        db = obtener_conexion()
        productos = db.execute('SELECT * FROM productos ORDER BY nombre ASC').fetchall()
        db.close()
        return productos

    @staticmethod
    def buscar_por_codigo(codigo):
        db = obtener_conexion()
        producto = db.execute('SELECT * FROM productos WHERE codigo_barras = ?', (codigo,)).fetchone()
        db.close()
        return producto

    @staticmethod
    def insertar(datos):
        db = obtener_conexion()
        db.execute('''INSERT INTO productos 
                      (codigo_barras, nombre, categoria, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', datos)
        db.commit()
        db.close()

    @staticmethod
    def actualizar_stock(codigo, cantidad_vendida):
        db = obtener_conexion()
        db.execute('UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?', (cantidad_vendida, codigo))
        db.commit()
        db.close()