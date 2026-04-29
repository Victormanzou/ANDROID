from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

from models import Producto, Venta, Compra

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
        try:
            if hasattr(Venta, "obtener_recientes"):
                ventas_recientes = Venta.obtener_recientes(10) or []
                ventas_recientes = [dict(v) for v in ventas_recientes]
        except:
            ventas_recientes = []

        abc_productos = []
        try:
            if hasattr(Producto, "analisis_abc"):
                abc_productos = Producto.analisis_abc() or []
        except:
            abc_productos = []

        metricas = {
            "ventas_hoy": resumen_hoy.get("total", 0),
            "utilidad_hoy": resumen_hoy.get("utilidad", 0),
            "conteo_stock_bajo": len(stock_bajo),
            "mermas_mes": 0
        }

        alertas = [
            {
                "tipo": "Stock",
                "mensaje": f"{p.get('nombre','Producto')} bajo stock",
                "color": "warning",
                "fecha": "Hoy"
            }
            for p in stock_bajo
        ]

        # =========================
        # FINANZAS SEGURAS (INDEX MINI)
        # =========================
        ingresos = metricas["ventas_hoy"]
        gastos = 0

        try:
            from database.conexion import obtener_conexion
            db = obtener_conexion()

            try:
                gastos = db.execute("""
                    SELECT COALESCE(SUM(cantidad * costo_unitario), 0)
                    FROM compras
                """).fetchone()[0]
            except:
                gastos = 0

            db.close()

        except:
            gastos = 0

        utilidad = ingresos - gastos

        return render_template(
            "index.html",
            metricas=metricas,
            alertas=alertas,
            productos_vencidos=productos_vencidos,
            ventas_recientes=ventas_recientes,
            abc_productos=abc_productos,

            ingresos=ingresos,
            gastos=gastos,
            utilidad=utilidad
        )

    except Exception as e:
        return f"ERROR INDEX: {str(e)}"


# =========================
# VENTAS POR HORA
# =========================
@app.route('/api/ventas_por_hora')
def ventas_por_hora():
    try:
        from database.conexion import obtener_conexion
        conn = obtener_conexion()

        rows = conn.execute("""
            SELECT 
                strftime('%H', fecha) as hora,
                COALESCE(SUM(total),0) as total
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
# FINANZAS (100% COMPATIBLE CON TU HTML)
# =========================
@app.route('/finanzas')
def finanzas():
    ingresos = 0
    gastos = 0

    try:
        from database.conexion import obtener_conexion
        db = obtener_conexion()

        # INGRESOS
        try:
            ingresos = db.execute("""
                SELECT COALESCE(SUM(total),0)
                FROM ventas
            """).fetchone()[0]
        except:
            ingresos = 0

        # GASTOS (SAFE)
        try:
            gastos = db.execute("""
                SELECT COALESCE(SUM(cantidad * costo_unitario),0)
                FROM compras
            """).fetchone()[0]
        except:
            gastos = 0

        db.close()

    except:
        ingresos = 0
        gastos = 0

    # =========================
    # CUENTAS SIMULADAS (PARA TU TABLA)
    # =========================
    cuentas = [
        {
            "proveedor": "General",
            "monto": gastos,
            "vence": datetime.now().strftime("%Y-%m-%d"),
            "estado": "Normal"
        }
    ] if gastos else []

    resumen = {
        "ingresos_mes": ingresos,
        "egresos_mes": gastos,
        "balance": ingresos - gastos
    }

    return render_template(
        "finanzas.html",
        resumen=resumen,
        cuentas=cuentas
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)