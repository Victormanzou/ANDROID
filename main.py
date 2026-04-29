from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os

from models import Producto, Venta, Merma, Compra, Categoria

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True


# =========================
# DASHBOARD
# =========================
@app.route('/')
def index():
    try:
        productos = Producto.obtener_todos() or []
        productos = [dict(p) for p in productos]

        stock_bajo = [
            p for p in productos
            if p.get('stock', 0) <= p.get('stock_minimo', 0)
        ]

        productos_vencidos = [
            p for p in productos
            if p.get('fecha_vencimiento')
        ]

        resumen_hoy = Venta.obtener_resumen_hoy() or {}

        ventas_recientes = []
        if hasattr(Venta, "obtener_recientes"):
            ventas_recientes = Venta.obtener_recientes(10) or []

        metricas = {
            'ventas_hoy': resumen_hoy.get('total', 0),
            'utilidad_hoy': resumen_hoy.get('utilidad', 0),
            'conteo_stock_bajo': len(stock_bajo),
            'mermas_mes': 50.00
        }

        alertas = [
            {
                'tipo': 'Stock',
                'mensaje': f"{p.get('nombre','Producto')} bajo stock",
                'color': 'warning',
                'fecha': 'Hoy'
            }
            for p in stock_bajo
        ]

        return render_template(
            'index.html',
            metricas=metricas,
            alertas=alertas,
            productos_vencidos=productos_vencidos,
            ventas_recientes=ventas_recientes,
            finanzas={},
            reporte_diario={},
            reporte_semanal={}
        )

    except Exception as e:
        return f"ERROR INDEX: {str(e)}"


# =========================
# 📊 NUEVO: VENTAS POR HORA (TIEMPO REAL)
# =========================
@app.route('/api/ventas_por_hora')
def ventas_por_hora():
    try:
        db = Venta.obtener_resumen_hoy

        from database.conexion import obtener_conexion
        conn = obtener_conexion()

        rows = conn.execute("""
            SELECT 
                strftime('%H', fecha) as hora,
                SUM(total) as total
            FROM ventas
            WHERE DATE(fecha) = DATE('now')
            GROUP BY hora
            ORDER BY hora
        """).fetchall()

        conn.close()

        datos = {f"{i:02d}": 0 for i in range(24)}

        for r in rows:
            datos[r["hora"]] = r["total"] or 0

        return jsonify(datos)

    except Exception as e:
        return jsonify({"error": str(e)})


# =========================
# INVENTARIO
# =========================
@app.route('/inventario')
def inventario():
    productos = Producto.obtener_todos() or []
    productos = [dict(p) for p in productos]

    return render_template('inventario.html', productos=productos)


@app.route('/inventario/agregar', methods=['POST'])
def agregar_producto():
    try:
        datos = (
            request.form.get('codigo'),
            request.form.get('nombre'),
            request.form.get('categoria'),
            float(request.form.get('p_compra') or 0),
            float(request.form.get('p_venta') or 0),
            int(request.form.get('stock') or 0),
            int(request.form.get('stock_min') or 5),
            request.form.get('vencimiento')
        )

        Producto.insertar(datos)
        return redirect(url_for('inventario'))

    except Exception as e:
        return f"Error inventario: {str(e)}"


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())


@app.route('/buscar_producto/<codigo>')
def buscar_producto(codigo):
    producto = Producto.buscar_por_codigo(codigo)

    if not producto:
        return jsonify({'success': False})

    return jsonify({
        'success': True,
        'producto': {
            'codigo_barras': producto['codigo_barras'],
            'nombre': producto['nombre'],
            'precio_venta': producto['precio_venta'],
            'stock': producto['stock']
        }
    })


@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    data = request.get_json()
    carrito = data.get('carrito', [])

    if not carrito:
        return jsonify({'success': False, 'message': 'Carrito vacío'})

    try:
        total = Venta.registrar_transaccion(carrito)

        return jsonify({
            'success': True,
            'total': total
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# =========================
# COMPRAS
# =========================
@app.route('/compras')
def compras():
    productos = Producto.obtener_todos() or []
    productos = [dict(p) for p in productos]

    return render_template('compras.html', productos=productos)


@app.route('/compras/agregar', methods=['POST'])
def agregar_compra():
    try:
        codigo = request.form.get('id_producto')
        cantidad = int(request.form.get('cantidad'))
        costo = float(request.form.get('costo_unitario'))

        Compra.registrar_entrada(codigo, cantidad, costo)
        return redirect(url_for('compras'))

    except Exception as e:
        return f"Error compras: {str(e)}"


# =========================
# FINANZAS
# =========================
@app.route('/finanzas')
def finanzas():
    return render_template('finanzas.html')


# =========================
# RUN
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)