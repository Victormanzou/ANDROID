from database.conexion import obtener_conexion

db = obtener_conexion()
try:
    # Intentamos insertar uno manualmente para probar
    db.execute('''INSERT INTO productos (codigo_barras, nombre, categoria, precio_compra, precio_venta, stock, stock_minimo) 
                  VALUES ('001', 'Producto de Prueba', 'Abarrotes', 10, 15, 20, 5)''')
    db.commit()
    print("¡Producto de prueba insertado con éxito!")
except Exception as e:
    print(f"Error o el producto ya existe: {e}")
finally:
    db.close()