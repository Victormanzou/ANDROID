from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os

# IMPORTANTE: Traemos nuestros modelos
from models import Producto, Venta, Merma, Compra, Categoria

app = Flask(__name__)

# --- RUTA: DASHBOARD PRINCIPAL ---
@app.route('/')
def index():
    productos = Producto.obtener_todos()
    
    stock_bajo = [p for p in productos if p['stock'] <= p['stock_minimo']]
    productos_vencidos = [p for p in productos if p['fecha_vencimiento'] and p['fecha_vencimiento'] != ""]

    resumen_hoy = Venta.obtener_resumen_hoy()
    
    metricas = {
        'ventas_hoy': resumen_hoy['total'] if resumen_hoy['total'] else 0.0,
        'utilidad_hoy': resumen_hoy['utilidad'] if resumen_hoy['utilidad'] else 0.0,
        'conteo_stock_bajo': len(stock_bajo),
        'mermas_mes': 50.00
    }
    
    alertas = [
        {
            'tipo': 'Stock',
            'mensaje': f"'{p['nombre']}' bajo stock.",
            'color': 'warning',
            'fecha': 'Hoy'
        } for p in stock_bajo
    ]
    
    finanzas = {
        'ingresos_mes': 15200.00,
        'egresos_mes': 8400.00,
        'porcentaje_gastos': 55
    }

    reporte_diario = {
        'horas': ['8AM', '12PM', '4PM', '8PM'],
        'ventas': [200, 800, 450, 950]
    }

    reporte_semanal = {
        'dias': ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
        'ventas': [1200, 1900, 1550, 2100, 3400, 4800, 4200]
    }

    return render_template(
        'index.html',
        metricas=metricas,
        alertas=alertas,
        productos_abc=[],
        productos_vencidos=productos_vencidos,
        finanzas=finanzas,
        reporte_diario=reporte_diario,
        reporte_semanal=reporte_semanal
    )

# --- INVENTARIO ---
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

# --- VENTAS ---
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())

@app.route('/buscar_producto/<codigo>')
def buscar_producto(codigo):
    producto = Producto.buscar_por_codigo(codigo)
    if producto:
        return jsonify({
            'success': True,
            'producto': {
                'codigo_barras': producto['codigo_barras'],
                'nombre': producto['nombre'],
                'precio_venta': producto['precio_venta'],
                'stock': producto['stock']
            }
        })
    return jsonify({'success': False})

@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    data = request.get_json()
    carrito = data.get('carrito', [])

    if not carrito:
        return jsonify({'success': False, 'message': 'Carrito vacío'})

    try:
        total = Venta.registrar_transaccion(carrito)
        return jsonify({'success': True, 'total': total})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# --- FINANZAS ---
@app.route('/finanzas')
def finanzas():
    resumen = {
        'ingresos_mes': 45000.0,
        'egresos_mes': 32000.0,
        'balance': 13000.0
    }
    return render_template('finanzas.html', resumen=resumen)

# --- COMPRAS ---
@app.route('/compras')
def compras():
    return render_template('compras.html')


# 🔥 IMPORTANTE PARA RAILWAY Y LOCAL
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)