-- Tabla de Productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    categoria TEXT,
    precio_compra REAL DEFAULT 0,
    precio_venta REAL DEFAULT 0,
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    fecha_vencimiento DATE
);

-- Tabla de Ventas (Cabecera)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL DEFAULT 0,
    utilidad REAL DEFAULT 0
);

-- Tabla de Gastos/Egresos
CREATE TABLE IF NOT EXISTS finanzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    tipo TEXT -- 'Ingreso' o 'Egreso'
);

-- Tabla de Proveedores (Cuentas por pagar)
CREATE TABLE IF NOT EXISTS cuentas_pagar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor TEXT NOT NULL,
    monto REAL NOT NULL,
    vence DATE,
    estado TEXT DEFAULT 'Pendiente' -- 'Pendiente', 'Urgente', 'Pagado'
);
-- Tabla de Compras
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    codigo_barras TEXT NOT NULL,
    proveedor TEXT,
    cantidad INTEGER NOT NULL,
    costo_unitario REAL NOT NULL,
    total REAL NOT NULL
);