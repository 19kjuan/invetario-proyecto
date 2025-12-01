#!/usr/bin/env python3
"""
Script para configurar la base de datos usando Python en lugar de comandos MySQL
"""

import pymysql
from app import create_app, db
from app.models import Usuario, Producto, Venta, DetalleVenta, Configuracion

def setup_database():
    """Configura la base de datos usando Python"""
    print("Configurando base de datos con Python...")
    
    try:
        # Conectar a MySQL y crear la base de datos
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Anne@nn8byte',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Crear la base de datos
            cursor.execute("DROP DATABASE IF EXISTS inventario_deportivo")
            cursor.execute("CREATE DATABASE inventario_deportivo")
            print("Base de datos 'inventario_deportivo' creada exitosamente")
            
            # Usar la base de datos
            cursor.execute("USE inventario_deportivo")
            
            # Crear tabla de productos
            cursor.execute("""
                CREATE TABLE productos (
                    id_producto INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10,2) NOT NULL,
                    stock INT NOT NULL DEFAULT 0,
                    categoria ENUM('Tenis','Pádel','Accesorios') DEFAULT 'Accesorios',
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("Tabla 'productos' creada exitosamente")
            
            # Crear tabla de ventas
            cursor.execute("""
                CREATE TABLE ventas (
                    id_venta INT AUTO_INCREMENT PRIMARY KEY,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total DECIMAL(10,2) NOT NULL
                )
            """)
            print("Tabla 'ventas' creada exitosamente")
            
            # Crear tabla de detalle de ventas
            cursor.execute("""
                CREATE TABLE detalle_ventas (
                    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
                    id_venta INT NOT NULL,
                    id_producto INT NOT NULL,
                    cantidad INT NOT NULL,
                    precio_unitario DECIMAL(10,2) NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE RESTRICT
                )
            """)
            print("Tabla 'detalle_ventas' creada exitosamente")
            
            # Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(64) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255),
                    es_admin BOOLEAN DEFAULT FALSE,
                    activo BOOLEAN DEFAULT TRUE,
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tabla 'usuarios' creada exitosamente")
            
            # Crear tabla de configuraciones
            cursor.execute("""
                CREATE TABLE configuraciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    clave VARCHAR(50) UNIQUE NOT NULL,
                    valor VARCHAR(200),
                    descripcion VARCHAR(200)
                )
            """)
            print("Tabla 'configuraciones' creada exitosamente")
            
            # Crear trigger para actualizar stock
            cursor.execute("""
                CREATE TRIGGER descontar_stock
                AFTER INSERT ON detalle_ventas
                FOR EACH ROW
                BEGIN
                    UPDATE productos
                    SET stock = stock - NEW.cantidad
                    WHERE id_producto = NEW.id_producto;
                END
            """)
            print("Trigger 'descontar_stock' creado exitosamente")
            
            # Insertar datos de ejemplo
            productos_ejemplo = [
                ('Raqueta Tenis Wilson Pro Staff', 'Raqueta profesional para tenis avanzado', 350.00, 10, 'Tenis'),
                ('Raqueta Pádel Bullpadel Vertex', 'Raqueta de pádel de alta gama', 280.00, 15, 'Pádel'),
                ('Pelotas Tenis Head (tubo x3)', 'Tubo con 3 pelotas presurizadas', 8.50, 100, 'Tenis'),
                ('Pelotas Pádel Dunlop (pack x3)', 'Pack de 3 pelotas de pádel', 7.00, 80, 'Pádel'),
                ('Grip Antideslizante', 'Grip universal para raquetas', 4.00, 50, 'Accesorios'),
                ('Bolso Wilson Super Tour', 'Bolso grande para raquetas y accesorios', 120.00, 20, 'Accesorios')
            ]
            
            for producto in productos_ejemplo:
                cursor.execute("""
                    INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                """, producto)
            
            print("Datos de ejemplo insertados exitosamente")
            
            # Crear una venta de ejemplo
            cursor.execute("INSERT INTO ventas (total) VALUES (367.00)")
            venta_id = cursor.lastrowid
            
            # Insertar detalles de la venta
            detalles_venta = [
                (venta_id, 3, 3, 8.50, 25.50),
                (venta_id, 5, 1, 4.00, 4.00),
                (venta_id, 1, 1, 350.00, 350.00)
            ]
            
            for detalle in detalles_venta:
                cursor.execute("""
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, detalle)
            
            print("Venta de ejemplo creada exitosamente")
            
        connection.commit()
        connection.close()
        
        print("Base de datos configurada exitosamente!")
        return True
        
    except Exception as e:
        print(f"Error al configurar la base de datos: {e}")
        return False

def create_admin_user():
    """Crea el usuario administrador"""
    print("Creando usuario administrador...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar si ya existe
            admin = Usuario.query.filter_by(email='admin@inventario.com').first()
            if admin:
                print("Usuario administrador ya existe")
                return True
            
            # Crear usuario administrador
            admin = Usuario(
                nombre_usuario='admin',
                email='admin@inventario.com',
                es_admin=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("Usuario administrador creado exitosamente")
            print("Email: admin@inventario.com")
            print("Contrasena: admin123")
            return True
            
    except Exception as e:
        print(f"Error al crear usuario administrador: {e}")
        return False

def main():
    """Función principal"""
    print("Configurando aplicacion de inventario deportivo...")
    
    # 1. Configurar base de datos
    if not setup_database():
        print("Error al configurar la base de datos")
        return False
    
    # 2. Crear usuario administrador
    if not create_admin_user():
        print("Error al crear usuario administrador")
        return False
    
    print("\nConfiguracion completada exitosamente!")
    print("\nResumen:")
    print("- Base de datos 'inventario_deportivo' creada")
    print("- Tablas creadas con datos de ejemplo")
    print("- Usuario administrador creado")
    print("- Trigger de actualizacion de stock configurado")
    
    print("\nPara ejecutar la aplicacion:")
    print("python run.py")
    print("\nLa aplicacion estara disponible en: http://localhost:5000")
    print("\nCredenciales de acceso:")
    print("Email: admin@inventario.com")
    print("Contrasena: admin123")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nLa configuracion fallo. Revisa los errores anteriores.")
        exit(1)
    else:
        print("\nConfiguracion exitosa! Puedes ejecutar la aplicacion ahora.")
