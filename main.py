from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os

from models import Producto, Venta

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


# =========================
# INDEX (SAFE)
# =========================
@app.route('/')
def index():
    try:
        productos = Producto.obtener_todos() or []

        resumen_hoy = Venta.obtener_resumen_hoy() or {}

        ingresos = resumen_hoy.get("total", 0)

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
# FINANZAS (NO CRASHEA NUNCA)
# =========================
@app.route('/finanzas')
def finanzas():
    try:
        from database.conexion import obtener_conexion
        db = obtener_conexion()

        ingresos = db.execute("SELECT COALESCE(SUM(total),0) FROM ventas").fetchone()[0] or 0

        gastos = 0
        try:
            gastos = db.execute("SELECT COALESCE(SUM(cantidad * costo_unitario),0) FROM compras").fetchone()[0] or 0
        except:
            gastos = 0

        db.close()

        resumen = {
            "ingresos_mes": ingresos,
            "egresos_mes": gastos,
            "balance": ingresos - gastos
        }

        return render_template("finanzas.html", resumen=resumen, cuentas=[])

    except Exception as e:
        return f"ERROR FINANZAS: {e}"


# =========================
# GUARDAR GASTO (SAFE)
# =========================
@app.route('/guardar_gasto', methods=['POST'])
def guardar_gasto():
    try:
        concepto = request.form.get("concepto")
        monto = request.form.get("monto")
        fecha = request.form.get("fecha")

        if not concepto or not monto:
            return redirect(url_for("finanzas"))

        try:
            from database.conexion import obtener_conexion
            db = obtener_conexion()

            db.execute("""
                INSERT INTO compras (proveedor, cantidad, costo_unitario, fecha)
                VALUES (?, 1, ?, ?)
            """, (concepto, float(monto), fecha))

            db.commit()
            db.close()
        except:
            pass

        return redirect(url_for("finanzas"))

    except Exception as e:
        return f"ERROR GASTO: {e}"


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)