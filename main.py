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

        return render_template(
            "index.html",
            metricas={"ventas_hoy": ingresos},
            ingresos=ingresos,
            gastos=0,
            utilidad=ingresos
        )

    except Exception as e:
        return f"ERROR INDEX: {str(e)}"


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())


@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    try:
        data = request.get_json(silent=True) or {}
        carrito = data.get("carrito", [])

        if not carrito:
            return jsonify({"success": False, "error": "Carrito vacío"})

        total = Venta.registrar_transaccion(carrito)

        return jsonify({"success": True, "total": total})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


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
        return render_template('inventario.html', productos=[])


# =========================
# COMPRAS
# =========================
@app.route('/compras')
def compras():
    return render_template("compras.html")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)