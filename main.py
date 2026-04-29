from flask import Flask, render_template, request, jsonify, redirect, url_for
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
        return f"ERROR INDEX: {e}"


# =========================
# INVENTARIO
# =========================
@app.route('/inventario')
def inventario():
    try:
        productos = Producto.obtener_todos() or []
        return render_template('inventario.html', productos=[dict(p) for p in productos])
    except:
        return render_template('inventario.html', productos=[])


# =========================
# VENTAS
# =========================
@app.route('/ventas')
def ventas():
    return render_template('ventas.html', now=datetime.now())


@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    try:
        data = request.get_json()
        carrito = data.get("carrito", [])

        if not carrito:
            return jsonify({"success": False})

        total = Venta.registrar_transaccion(carrito)
        return jsonify({"success": True, "total": total})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# =========================
# FINANZAS
# =========================
@app.route('/finanzas')
def finanzas():
    try:
        from database.conexion import obtener_conexion
        db = obtener_conexion()

        ingresos = db.execute("""
            SELECT COALESCE(SUM(total),0)
            FROM ventas
        """).fetchone()[0] or 0

        gastos = db.execute("""
            SELECT COALESCE(SUM(cantidad * costo_unitario),0)
            FROM compras
        """).fetchone()[0] or 0

        db.close()

    except:
        ingresos = 0
        gastos = 0

    resumen = {
        "ingresos_mes": float(ingresos),
        "egresos_mes": float(gastos),
        "balance": float(ingresos) - float(gastos)
    }

    return render_template("finanzas.html", resumen=resumen, cuentas=[])


# =========================
# GUARDAR GASTO (ARREGLADO)
# =========================
@app.route('/agregar_gasto', methods=['POST'])
def agregar_gasto():
    try:
        concepto = request.form.get("concepto", "Gasto")
        monto = float(request.form.get("monto") or 0)
        fecha = request.form.get("fecha") or datetime.now().strftime("%Y-%m-%d")

        from database.conexion import obtener_conexion
        db = obtener_conexion()

        db.execute("""
            INSERT INTO compras (proveedor, cantidad, costo_unitario, fecha)
            VALUES (?, 1, ?, ?)
        """, (concepto, monto, fecha))

        db.commit()
        db.close()

        return redirect(url_for("finanzas"))

    except Exception as e:
        return f"ERROR GASTO: {e}"


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)