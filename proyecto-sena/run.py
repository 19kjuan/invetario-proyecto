import os
from app import create_app, db
from app.models import Usuario, Producto, Venta, DetalleVenta, Cliente, MovimientoInventario, Configuracion

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Hace que estos objetos estén disponibles automáticamente en el shell de Flask"""
    return {
        'db': db,
        'Usuario': Usuario,
        'Producto': Producto,
        'Venta': Venta,
        'DetalleVenta': DetalleVenta,
        'Cliente': Cliente,
        'MovimientoInventario': MovimientoInventario,
        'Configuracion': Configuracion
    }

@app.cli.command()
def init_db():
    """Inicializa la base de datos con tablas y datos de ejemplo"""
    print("Creando tablas...")
    db.create_all()
    
    # Verificar si ya existe un usuario administrador
    admin = Usuario.query.filter_by(email='admin@inventario.com').first()
    if not admin:
        print("Creando usuario administrador...")
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@inventario.com',
            es_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print(f"Usuario administrador creado: admin@inventario.com / admin123")
    else:
        print("El usuario administrador ya existe.")
    
    # Agregar configuraciones por defecto
    configs = [
        ('umbral_alerta_stock', '5', 'Umbral para alertas de stock bajo'),
        ('moneda', 'COP', 'Moneda utilizada en el sistema'),
        ('nombre_negocio', 'Inventario Tenis & Pádel', 'Nombre del negocio'),
    ]
    
    for clave, valor, descripcion in configs:
        config = Configuracion.query.filter_by(clave=clave).first()
        if not config:
            Configuracion.set_config(clave, valor, descripcion)
    
    print("Base de datos inicializada correctamente!")

@app.cli.command()
def create_sample_data():
    """Crea datos de ejemplo para pruebas"""
    print("Creando datos de ejemplo...")
    
    # Verificar si ya existen productos
    if Producto.query.count() > 0:
        print("Ya existen productos en la base de datos.")
        return
    
    # Obtener el usuario admin
    admin = Usuario.query.filter_by(email='admin@inventario.com').first()
    if not admin:
        print("Error: No existe el usuario administrador. Ejecuta 'flask init-db' primero.")
        return
    
    # Crear productos de ejemplo
    productos_ejemplo = [
        {
            'codigo': 'RAQ-001',
            'nombre': 'Raqueta Wilson Pro Staff',
            'descripcion': 'Raqueta profesional de tenis, ideal para jugadores avanzados',
            'precio_compra': 350000,
            'precio_venta': 520000,
            'stock': 15,
            'stock_minimo': 3,
            'categoria': 'Tenis',
            'marca': 'Wilson',
            'color': 'Negro/Rojo'
        },
        {
            'codigo': 'RAQ-002',
            'nombre': 'Raqueta Head Graphene 360',
            'descripcion': 'Raqueta de pádel con tecnología Graphene 360',
            'precio_compra': 280000,
            'precio_venta': 420000,
            'stock': 12,
            'stock_minimo': 3,
            'categoria': 'Pádel',
            'marca': 'Head',
            'color': 'Azul/Blanco'
        },
        {
            'codigo': 'PEL-001',
            'nombre': 'Pelotas Wilson Championship',
            'descripcion': 'Tubo de 3 pelotas de tenis profesionales',
            'precio_compra': 12000,
            'precio_venta': 18000,
            'stock': 50,
            'stock_minimo': 10,
            'categoria': 'Accesorios',
            'marca': 'Wilson',
            'color': 'Amarillo'
        },
        {
            'codigo': 'ZAP-001',
            'nombre': 'Zapatillas Nike Court Air Zoom',
            'descripcion': 'Zapatillas de tenis con tecnología Air Zoom',
            'precio_compra': 180000,
            'precio_venta': 280000,
            'stock': 8,
            'stock_minimo': 2,
            'categoria': 'Tenis',
            'marca': 'Nike',
            'talla': '42',
            'color': 'Blanco'
        },
        {
            'codigo': 'BOL-001',
            'nombre': 'Bolso Head Tour Team',
            'descripcion': 'Bolso deportivo para raquetas y accesorios',
            'precio_compra': 95000,
            'precio_venta': 145000,
            'stock': 6,
            'stock_minimo': 2,
            'categoria': 'Accesorios',
            'marca': 'Head',
            'color': 'Negro/Azul'
        },
        {
            'codigo': 'GRI-001',
            'nombre': 'Grip Wilson Pro Overgrip',
            'descripcion': 'Pack de 3 overgrips profesionales',
            'precio_compra': 8000,
            'precio_venta': 15000,
            'stock': 30,
            'stock_minimo': 8,
            'categoria': 'Accesorios',
            'marca': 'Wilson',
            'color': 'Blanco'
        }
    ]
    
    for prod_data in productos_ejemplo:
        producto = Producto(**prod_data)
        db.session.add(producto)
        
        # Registrar movimiento de inventario inicial
        if prod_data['stock'] > 0:
            movimiento = MovimientoInventario(
                tipo='entrada',
                cantidad=prod_data['stock'],
                notas='Carga inicial de inventario',
                producto=producto,
                usuario_id=admin.id
            )
            db.session.add(movimiento)
    
    # Crear clientes de ejemplo
    clientes_ejemplo = [
        {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan.perez@example.com',
            'telefono': '3001234567',
            'direccion': 'Calle 123 #45-67'
        },
        {
            'nombre': 'María',
            'apellido': 'García',
            'email': 'maria.garcia@example.com',
            'telefono': '3009876543',
            'direccion': 'Carrera 45 #12-34'
        }
    ]
    
    for cliente_data in clientes_ejemplo:
        cliente = Cliente(**cliente_data)
        db.session.add(cliente)
    
    db.session.commit()
    print("Datos de ejemplo creados correctamente!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
