{% extends 'base.html' %}

{% block content %}
<div class="row mb-4 align-items-center">
    <div class="col-md-8">
        <h2 class="fw-bold m-0">📊 Panel de Inteligencia</h2>
        <p class="text-muted m-0">Supervisión detallada de la operación.</p>
    </div>
    <div class="col-md-4 text-md-end mt-3 mt-md-0">
        <button type="button" class="btn btn-info border-0 shadow-sm py-2 px-3 text-white position-relative" data-bs-toggle="modal" data-bs-target="#modalCaducidad" style="z-index: 1020;">
            <i class="bi bi-calendar-event-fill me-2"></i> 
            <strong>{{ productos_vencidos|length if productos_vencidos else "0" }}</strong> productos vencen pronto
            <span class="badge-pulse"></span>
        </button>
    </div>
</div>

<ul class="nav nav-pills nav-fill mb-4 bg-white shadow-sm p-1 rounded-pill" id="pills-tab" role="tablist" style="border: 1px solid #eee;">
    <li class="nav-item" role="presentation">
        <button class="nav-link active rounded-pill fw-bold" id="pills-hoy-tab" data-bs-toggle="pill" data-bs-target="#pills-hoy" type="button" role="tab">Operación Hoy</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link rounded-pill fw-bold" id="pills-semana-tab" data-bs-toggle="pill" data-bs-target="#pills-semana" type="button" role="tab">Análisis Semanal</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link rounded-pill fw-bold" id="pills-finanzas-tab" data-bs-toggle="pill" data-bs-target="#pills-finanzas" type="button" role="tab">Salud Financiera</button>
    </li>
</ul>

<div class="tab-content" id="pills-tabContent">
    
    <div class="tab-pane fade show active" id="pills-hoy" role="tabpanel">
        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 h-100">
                    <div class="d-flex align-items-center">
                        <div class="icon-shape bg-soft-primary text-primary rounded-circle me-3">
                            <i class="bi bi-currency-dollar fs-4"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 text-muted small text-uppercase fw-bold">Ventas</h6>
                            <h3 class="fw-bold mb-0">${{ "{:,.2f}".format(metricas.ventas_hoy) if metricas else "0.00" }}</h3>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 h-100 border-start border-success border-4">
                    <div class="d-flex align-items-center">
                        <div class="icon-shape bg-soft-success text-success rounded-circle me-3">
                            <i class="bi bi-graph-up-arrow fs-4"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 text-muted small text-uppercase fw-bold">Utilidad</h6>
                            <h3 class="fw-bold mb-0 text-success">${{ "{:,.2f}".format(metricas.utilidad_hoy) if metricas else "0.00" }}</h3>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 h-100">
                    <div class="d-flex align-items-center">
                        <div class="icon-shape bg-soft-warning text-warning rounded-circle me-3">
                            <i class="bi bi-box-seam fs-4"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 text-muted small text-uppercase fw-bold">Stock Bajo</h6>
                            <h3 class="fw-bold mb-0">{{ metricas.conteo_stock_bajo if metricas else "0" }}</h3>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 h-100">
                    <div class="d-flex align-items-center">
                        <div class="icon-shape bg-soft-danger text-danger rounded-circle me-3">
                            <i class="bi bi-trash fs-4"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 text-muted small text-uppercase fw-bold">Mermas</h6>
                            <h3 class="fw-bold mb-0 text-danger">${{ "{:,.2f}".format(metricas.mermas_mes) if metricas else "0.00" }}</h3>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-lg-8">
                <div class="card shadow-sm border-0 h-100">
                    <div class="card-header bg-white py-3 d-flex justify-content-between">
                        <h5 class="mb-0 fw-bold"><i class="bi bi-clock-history text-primary"></i> Flujo de Ventas por Hora</h5>
                        <span class="badge bg-soft-primary text-primary">Hoy</span>
                    </div>
                    <div class="card-body">
                        <canvas id="graficaHoras" height="280"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card shadow-sm border-0 h-100 bg-light">
                    <div class="card-body">
                        <h5 class="fw-bold mb-3"><i class="bi bi-lightning-charge text-warning"></i> Alertas Hoy</h5>
                        <ul class="list-group list-group-flush bg-transparent">
                            {% for alerta in alertas %}
                            <li class="list-group-item bg-transparent px-0 border-0 mb-2">
                                <div class="d-flex align-items-center mb-1">
                                    <span class="badge bg-{{ alerta.color }} me-2">{{ alerta.tipo }}</span>
                                    <small class="text-muted">{{ alerta.fecha }}</small>
                                </div>
                                <span class="small fw-bold">{{ alerta.mensaje }}</span>
                            </li>
                            {% else %}
                            <li class="list-group-item bg-transparent text-center text-muted py-5 border-0">
                                <i class="bi bi-check2-circle fs-1 d-block mb-2 text-success"></i>
                                Todo en orden.
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="tab-pane fade" id="pills-semana" role="tabpanel">
        <div class="row g-4">
            <div class="col-lg-12 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-header bg-white py-3">
                        <h5 class="mb-0 fw-bold"><i class="bi bi-graph-up-arrow text-primary"></i> Tendencia y Predicción de la Semana</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="graficaVentas" height="300"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="card shadow-sm border-0">
                    <div class="card-header bg-white py-3 text-primary fw-bold">
                        <i class="bi bi-pie-chart me-2"></i>Análisis ABC: Rentabilidad por Producto
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle mb-0 text-center">
                                <thead class="table-light small text-uppercase">
                                    <tr>
                                        <th class="ps-4 text-start">Producto</th>
                                        <th>Clase ABC</th>
                                        <th>Margen</th>
                                        <th>Estado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for prod in productos_abc %}
                                    <tr>
                                        <td class="ps-4 fw-medium text-start">{{ prod.nombre }}</td>
                                        <td><span class="badge bg-primary rounded-pill px-3">{{ prod.clase }}</span></td>
                                        <td>{{ prod.margen }}%</td>
                                        <td>
                                            {% if prod.margen >= 25 %} <span class="text-success fw-bold">🟢 Alta</span>
                                            {% elif prod.margen >= 15 %} <span class="text-warning fw-bold">🟡 Media</span>
                                            {% else %} <span class="text-danger fw-bold">🔴 Baja</span>
                                            {% endif %}
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="tab-pane fade" id="pills-finanzas" role="tabpanel">
        <div class="row g-4">
            <div class="col-md-6">
                <div class="card shadow-sm border-0 p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="fw-bold m-0"><i class="bi bi-wallet2 text-primary me-2"></i>Flujo de Caja Mensual</h5>
                        <a href="{{ url_for('finanzas') }}" class="btn btn-sm btn-outline-primary rounded-pill px-3">Administrar</a>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span class="small text-muted">Ingresos: ${{ "{:,.2f}".format(finanzas.ingresos_mes) if finanzas else "0.00" }}</span>
                        <span class="small text-muted">Gastos: ${{ "{:,.2f}".format(finanzas.egresos_mes) if finanzas else "0.00" }}</span>
                    </div>
                    <div class="progress mb-3" style="height: 25px; border-radius: 12px; background: #eee;">
                        <div class="progress-bar custom-progress" role="progressbar" 
                             style="--progreso: {{ finanzas.porcentaje_gastos | default(0) }}%;" 
                             aria-valuenow="{{ finanzas.porcentaje_gastos | default(0) }}" 
                             aria-valuemin="0" aria-valuemax="100">
                             Gastos {{ finanzas.porcentaje_gastos | default(0) }}%
                        </div>
                    </div>
                    <p class="small text-center {% if finanzas and finanzas.porcentaje_gastos > 80 %}text-danger{% else %}text-success{% endif %} fw-bold mt-2">
                        {% if finanzas and finanzas.porcentaje_gastos > 80 %}
                            ⚠️ Los gastos están consumiendo tu utilidad.
                        {% else %}
                            ✅ Balance financiero saludable.
                        {% endif %}
                    </p>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card shadow-sm border-0 h-100">
                    <div class="card-header bg-white py-3 border-0 d-flex justify-content-between align-items-center">
                        <h5 class="mb-0 fw-bold"><i class="bi bi-truck text-danger me-2"></i>Cuentas por Pagar</h5>
                        <a href="{{ url_for('finanzas') }}" class="btn btn-sm btn-soft-danger rounded-pill px-3">Gestionar</a>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                            {% for cuenta in cuentas_pagar %}
                            <li class="list-group-item d-flex justify-content-between align-items-center py-3 border-0">
                                <div><span class="fw-bold d-block">{{ cuenta['proveedor'] }}</span><small class="text-muted">Vence: {{ cuenta['vence'] }}</small></div>
                                <div class="text-end">
                                    <span class="fw-bold d-block text-danger">${{ "{:,.2f}".format(cuenta['monto']) }}</span>
                                    <span class="badge bg-{{ 'danger' if cuenta['estado'] == 'Urgente' else 'warning text-dark' }} rounded-pill small">
                                        {{ cuenta['estado'] }}
                                    </span>
                                </div>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="modalCaducidad" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
            <div class="modal-header bg-info text-white border-0">
                <h5 class="modal-title fw-bold">Próximos Vencimientos</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-0">
                <ul class="list-group list-group-flush">
                    {% for p in productos_vencidos %}
                    <li class="list-group-item d-flex justify-content-between align-items-center py-3">
                        <div>
                            <span class="fw-bold d-block">{{ p['nombre'] }}</span>
                            <small class="text-muted">Expira el: {{ p['fecha_vencimiento'] }}</small>
                        </div>
                        <span class="badge bg-warning text-dark rounded-pill">Vence pronto</span>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // GRÁFICA DE HORAS PICO
    const ctxHoras = document.getElementById('graficaHoras');
    new Chart(ctxHoras, {
        type: 'bar',
        data: {
            labels: ['8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM', '10 PM'],
            datasets: [{
                label: 'Flujo de Ventas ($)',
                data: [450, 300, 1200, 1800, 950, 2100, 2800, 1500],
                backgroundColor: 'rgba(99, 102, 241, 0.7)',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { callback: v => '$' + v } } }
        }
    });

    // GRÁFICA SEMANAL
    const ctxSemana = document.getElementById('graficaVentas');
    new Chart(ctxSemana, {
        type: 'line',
        data: {
            labels: ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
            datasets: [
                { label: 'Ventas Reales', data: [1200, 1900, 1550, 2100, 3400, 4800, 4200], borderColor: '#6366f1', backgroundColor: 'rgba(99, 102, 241, 0.1)', fill: true, tension: 0.4 },
                { label: 'Predicción', data: [1100, 1800, 1600, 2000, 3100, 4800, 4200], borderColor: '#a855f7', borderDash: [5, 5], fill: false, tension: 0.4 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
});
</script>
{% endblock %}