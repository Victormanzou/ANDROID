from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os

from models import Producto, Venta

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True


# =========================
# INDEX
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
            p for p in productos if p.get('fecha_vencimiento')
        ]

        resumen_hoy = Venta.obtener_resumen_hoy() or {}

        metricas = {
            "ventas_hoy": resumen_hoy.get("total", 0),
            "utilidad_hoy": resumen_hoy.get("utilidad", 0),
            "conteo_stock_bajo": len(stock_bajo),
            "mermas_mes": 0
        }

        ingresos = metricas["ventas_hoy"]
        gastos = 0

        try:
            from database.conexion import obtener_conexion
            db = obtener_conexion()

            row = db.execute("""
                SELECT COALESCE(SUM(cantidad * costo_unitario),0)
                FROM compras
            """).fetchone()

            gastos = row[0] if row else 0

            db.close()

        except:
            gastos = 0

        return render_template(
            "index.html",
            metricas=metricas,
            productos_vencidos=productos_vencidos,
            ingresos=ingresos,
            gastos=gastos,
            utilidad=ingresos - gastos
        )

    except Exception as e:
        return f"ERROR INDEX: {str(e)}"


# =========================
# INVENTARIO
# =========================
@app.route('/inventario')
def inventario():
    productos = Producto.obtener_todos() or []
    return render_template('inventario.html', productos=[dict(p) for p in productos])


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())


@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    data = request.get_json()
    carrito = data.get("carrito", [])

    if not carrito:
        return jsonify({"success": False})

    total = Venta.registrar_transaccion(carrito)
    return jsonify({"success": True, "total": total})


# =========================
# COMPRAS
# =========================
@app.route('/compras')
def compras():
    productos = Producto.obtener_todos() or []
    return render_template('compras.html', productos=[dict(p) for p in productos])


# =========================
# FINANZAS
# =========================
@app.route('/finanzas')
def finanzas():
    ingresos = 0
    gastos = 0

    try:
        from database.conexion import obtener_conexion
        db = obtener_conexion()

        row1 = db.execute("""
            SELECT COALESCE(SUM(total),0) FROM ventas
        """).fetchone()
        ingresos = row1[0] if row1 else 0

        try:
            row2 = db.execute("""
                SELECT COALESCE(SUM(cantidad * costo_unitario),0)
                FROM compras
            """).fetchone()
            gastos = row2[0] if row2 else 0
        except:
            gastos = 0

        db.close()

    except:
        ingresos = 0
        gastos = 0

    resumen = {
        "ingresos_mes": ingresos,
        "egresos_mes": gastos,
        "balance": ingresos - gastos
    }

    return render_template("finanzas.html", resumen=resumen)


# =========================
# GUARDAR GASTO (100% FUNCIONAL)
# =========================
@app.route('/guardar_gasto', methods=['POST'])
def guardar_gasto():
    try:
        concepto = request.form.get("concepto")
        monto = request.form.get("monto")
        fecha = request.form.get("fecha")

        if not concepto or not monto:
            return redirect(url_for('finanzas'))

        monto = float(monto)

        from database.conexion import obtener_conexion
        db = obtener_conexion()

        db.execute("""
            INSERT INTO compras (proveedor, cantidad, costo_unitario, fecha)
            VALUES (?, 1, ?, ?)
        """, (concepto, monto, fecha))

        db.commit()
        db.close()

        return redirect(url_for('finanzas'))

    except Exception as e:
        return f"ERROR GUARDAR GASTO: {str(e)}"


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)