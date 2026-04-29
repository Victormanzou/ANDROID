from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os

from models import Producto, Venta, Merma, Compra, Categoria

app = Flask(__name__)

# 🔥 CACHE FIX
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True


# =========================
# DASHBOARD
# =========================
@app.route('/')
def index():
    productos = Producto.obtener_todos()

    stock_bajo = [p for p in productos if p['stock'] <= p['stock_minimo']]
    productos_vencidos = [p for p in productos if p.get('fecha_vencimiento')]

    # 🔥 FIX CRÍTICO
    resumen_hoy = Venta.obtener_resumen_hoy() or {}

    metricas = {
        'ventas_hoy': resumen_hoy.get('total', 0.0),
        'utilidad_hoy': resumen_hoy.get('utilidad', 0.0),
        'conteo_stock_bajo': len(stock_bajo),
        'mermas_mes': 50.00
    }

    alertas = [{
        'tipo': 'Stock',
        'mensaje': f"{p['nombre']} bajo stock",
        'color': 'warning',
        'fecha': 'Hoy'
    } for p in stock_bajo]

    return render_template(
        'index.html',
        metricas=metricas,
        alertas=alertas,
        productos_abc=[],
        productos_vencidos=productos_vencidos,
        finanzas={},
        reporte_diario={},
        reporte_semanal={}
    )


# =========================
# INVENTARIO
# =========================
@app.route('/inventario')
def inventario():
    productos = Producto.obtener_todos()
    return render_template('inventario.html', productos=productos)


@app.route('/inventario/agregar', methods=['POST'])
def agregar_producto():
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


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())


@app.route('/buscar_producto/<codigo>')
def buscar_producto(codigo):
    producto = Producto.buscar_por_codigo(codigo)

    if producto:
        return jsonify({
            'success': True,
            'producto': producto
        })

    return jsonify({'success': False})


@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    data = request.get_json()
    carrito = data.get('carrito', [])

    if not carrito:
        return jsonify({'success': False})

    try:
        total = Venta.registrar_transaccion(carrito)
        return jsonify({'success': True, 'total': total})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# =========================
# COMPRAS
# =========================
@app.route('/compras')
def compras():
    productos = Producto.obtener_todos()
    compras = Compra.obtener_todas() if hasattr(Compra, "obtener_todas") else []

    return render_template(
        'compras.html',
        productos=productos,
        compras=compras
    )


@app.route('/compras/agregar', methods=['POST'])
def agregar_compra():
    try:
        id_producto = request.form.get('id_producto')
        proveedor = request.form.get('proveedor')
        cantidad = int(request.form.get('cantidad'))
        costo = float(request.form.get('costo_unitario'))

        total = cantidad * costo

        Compra.registrar((id_producto, proveedor, cantidad, costo, total))
        Producto.aumentar_stock(id_producto, cantidad)

        return redirect(url_for('compras'))

    except Exception as e:
        return f"Error: {str(e)}"


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