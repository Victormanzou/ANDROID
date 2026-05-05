from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

from models import Producto, Venta

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


# =========================
# INDEX
# =========================
@app.route('/')
def index():

    try:
        resumen_hoy = Venta.obtener_resumen_hoy() or {}

        ingresos = float(resumen_hoy.get("total") or 0)

        productos = Producto.obtener_todos() or []

        return render_template(
            "index.html",

            metricas={
                "ventas_hoy": ingresos,
                "utilidad_hoy": ingresos,
                "conteo_stock_bajo": 0,
                "mermas_mes": 0
            },

            alertas=[],
            productos_vencidos=[],
            ventas_recientes=[],
            abc_productos=[],

            ingresos=ingresos,
            gastos=0,
            utilidad=ingresos,

            reporte_semanal=[0,0,0,0,0,0,0]
        )

    except Exception as e:
        return f"ERROR INDEX: {str(e)}"


# =========================
# API VENTAS POR HORA
# =========================
@app.route('/api/ventas_por_hora')
def ventas_por_hora():

    datos = {
        "08": 0,
        "09": 0,
        "10": 0,
        "11": 0,
        "12": 0
    }

    return jsonify(datos)


# =========================
# INVENTARIO
# =========================
@app.route('/inventario')
def inventario():

    try:
        productos = Producto.obtener_todos() or []

        return render_template(
            'inventario.html',
            productos=[dict(p) for p in productos]
        )

    except:
        return render_template(
            'inventario.html',
            productos=[]
        )


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():

    return render_template(
        'ventas.html',
        now=datetime.now()
    )


# =========================
# FINALIZAR VENTA
# =========================
@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():

    try:
        data = request.get_json(silent=True) or {}

        carrito = data.get("carrito", [])

        if not carrito:
            return jsonify({"success": False})

        total = Venta.registrar_transaccion(carrito)

        return jsonify({
            "success": True,
            "total": total
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# =========================
# COMPRAS
# =========================
@app.route('/compras')
def compras():

    return render_template("compras.html")


# =========================
# FINANZAS
# =========================
@app.route('/finanzas')
def finanzas():

    return render_template(
        "finanzas.html",
        resumen={
            "ingresos_mes": 0,
            "egresos_mes": 0,
            "balance": 0
        },
        cuentas=[]
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )