"""
Script para crear el usuario administrador
"""
from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    # Verificar si ya existe un usuario administrador
    admin = Usuario.query.filter_by(email='admin@inventario.com').first()
    
    if admin:
        print("El usuario administrador ya existe.")
        print(f"Email: {admin.email}")
        print(f"Nombre de usuario: {admin.nombre_usuario}")
    else:
        print("Creando usuario administrador...")
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@inventario.com',
            es_admin=True,
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("\nUsuario administrador creado exitosamente!")
        print("=" * 50)
        print("Email: admin@inventario.com")
        print("Contrasena: admin123")
        print("=" * 50)
        print("\nAhora puedes iniciar sesion en: http://localhost:5000")
