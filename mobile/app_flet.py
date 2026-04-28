import sys
import os
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import flet as ft

# 1. AJUSTE DE PATH Y MODELOS
# Asegura que Python encuentre la carpeta de tus modelos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.producto import Producto 
    from models.venta import Venta
    from models import Merma, Compra, Categoria
except ImportError as e:
    print(f"⚠️ Aviso: Error al importar modelos: {e}")

# --- CONFIGURACIÓN DE FLASK ---
app = Flask(__name__)

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
    
    alertas = [{'tipo': 'Stock', 'mensaje': f"'{p['nombre']}' bajo stock.", 'color': 'warning', 'fecha': 'Hoy'} for p in stock_bajo]
    finanzas_data = {'ingresos_mes': 15200.00, 'egresos_mes': 8400.00, 'porcentaje_gastos': 55}
    reporte_diario = {'horas': ['8AM', '12PM', '4PM', '8PM'], 'ventas': [200, 800, 450, 950]}
    reporte_semanal = {'dias': ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'], 'ventas': [1200, 1900, 1550, 2100, 3400, 4800, 4200]}

    return render_template('index.html', 
                           metricas=metricas, 
                           alertas=alertas, 
                           productos_vencidos=productos_vencidos, 
                           finanzas=finanzas_data, 
                           reporte_diario=reporte_diario, 
                           reporte_semanal=reporte_semanal)

@app.route('/inventario')
def inventario():
    productos = Producto.obtener_todos()
    return render_template('inventario.html', productos=productos)

@app.route('/buscar_producto/<codigo>')
def buscar_producto(codigo):
    producto = Producto.buscar_por_codigo(codigo)
    if producto:
        return jsonify({'success': True, 'producto': producto})
    return jsonify({'success': False})

@app.route('/finalizar_venta', methods=['POST'])
def finalizar_venta():
    data = request.get_json()
    carrito = data.get('carrito', [])
    try:
        total = Venta.registrar_transaccion(carrito)
        return jsonify({'success': True, 'total': total})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# --- CONFIGURACIÓN DE FLET (INTERFAZ MÓVIL) ---
def main_flet(page: ft.Page):
    page.title = "PROYECTO ABA - Móvil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def on_scan_result(e):
        codigo_detectado = e.data
        input_codigo.value = codigo_detectado
        try:
            producto = Producto.buscar_por_codigo(codigo_detectado)
            if producto:
                txt_status.value = f"Producto: {producto['nombre']} - ${producto['precio_venta']}"
                txt_status.color = ft.colors.GREEN_700
            else:
                txt_status.value = "Producto no encontrado en inventario"
                txt_status.color = ft.colors.ORANGE
        except Exception as ex:
            txt_status.value = f"Error de base de datos: {str(ex)}"
            txt_status.color = ft.colors.RED
        page.update()

    scanner = ft.BarcodeScanner(on_result=on_scan_result)
    page.overlay.append(scanner)
    input_codigo = ft.TextField(label="Código de Barras", read_only=True)
    txt_status = ft.Text("Listo para escanear...", size=16)

    btn_scanner = ft.ElevatedButton(
        "ABRIR CÁMARA", icon=ft.icons.CAMERA_ALT,
        on_click=lambda _: scanner.scan(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    page.add(
        ft.Column([
            ft.Text("PROYECTO ABA", size=30, weight="bold", color=ft.colors.BLUE_900),
            ft.Text("Gestión de Inventario Móvil", size=18, color=ft.colors.BLUE_GREY_400),
            ft.Divider(),
            btn_scanner,
            input_codigo,
            txt_status,
            ft.ElevatedButton("REGISTRAR VENTA", 
                             icon=ft.icons.SHOPPING_CART, 
                             color=ft.colors.WHITE, 
                             bgcolor=ft.colors.BLUE_700)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

# --- LANZAMIENTO SINCRONIZADO ---
def run_flask():
    # IMPORTANTE: debug=False y use_reloader=False evitan el bucle de reinicio infinito
    print("\n[SERVIDOR] Flask activo en puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Limpiar la terminal para mayor claridad
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*60)
    print("       SISTEMA HÍBRIDO PROYECTO ABA (WEB + MÓVIL)")
    print("="*60)

    # 1. Iniciar Flask en un hilo independiente (segundo plano)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # 2. Pequeña pausa para permitir que Flask se asiente
    time.sleep(2)

    print(f"\n[*] PANEL WEB:   http://7.206.135.167:5000")
    print(f"[*] APP ANDROID: http://7.206.135.167:8550")
    print("\n" + "="*60)
    print("Esperando conexión desde la App de Flet en Android...")

    # 3. Lanzar Flet en puerto fijo 8550 para el celular
    ft.app(target=main_flet, view=ft.AppView.FLET_APP, port=8550)