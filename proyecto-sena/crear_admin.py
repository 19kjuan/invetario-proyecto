#!/usr/bin/env python3
"""
Script para crear el usuario administrador
"""

from app import create_app, db
from app.models import Usuario

def crear_admin():
    """Crea el usuario administrador si no existe"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe un usuario administrador
        admin = Usuario.query.filter_by(email='admin@inventario.com').first()
        
        if admin:
            print("✅ El usuario administrador ya existe")
            return True
        
        try:
            # Crear el usuario administrador
            admin = Usuario(
                nombre_usuario='admin',
                email='admin@inventario.com',
                es_admin=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente")
            print("📧 Email: admin@inventario.com")
            print("🔑 Contraseña: admin123")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear el usuario administrador: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    crear_admin()