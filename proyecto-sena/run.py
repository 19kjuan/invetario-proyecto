import os
from app import create_app, db
from app.models import Usuario, Producto, Venta, DetalleVenta, Configuracion

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
    
    # Crear productos de ejemplo
    productos_ejemplo = [
        {
            'nombre': 'Raqueta Tenis Wilson Pro Staff',
            'descripcion': 'Raqueta profesional para tenis avanzado',
            'precio': 350.00,
            'stock': 10,
            'categoria': 'Tenis'
        },
        {
            'nombre': 'Raqueta Pádel Bullpadel Vertex',
            'descripcion': 'Raqueta de pádel de alta gama',
            'precio': 280.00,
            'stock': 15,
            'categoria': 'Pádel'
        },
        {
            'nombre': 'Pelotas Tenis Head (tubo x3)',
            'descripcion': 'Tubo con 3 pelotas presurizadas',
            'precio': 8.50,
            'stock': 100,
            'categoria': 'Tenis'
        },
        {
            'nombre': 'Pelotas Pádel Dunlop (pack x3)',
            'descripcion': 'Pack de 3 pelotas de pádel',
            'precio': 7.00,
            'stock': 80,
            'categoria': 'Pádel'
        },
        {
            'nombre': 'Grip Antideslizante',
            'descripcion': 'Grip universal para raquetas',
            'precio': 4.00,
            'stock': 50,
            'categoria': 'Accesorios'
        },
        {
            'nombre': 'Bolso Wilson Super Tour',
            'descripcion': 'Bolso grande para raquetas y accesorios',
            'precio': 120.00,
            'stock': 20,
            'categoria': 'Accesorios'
        }
    ]
    
    for prod_data in productos_ejemplo:
        producto = Producto(**prod_data)
        db.session.add(producto)
    
    db.session.commit()
    print("Datos de ejemplo creados correctamente!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
