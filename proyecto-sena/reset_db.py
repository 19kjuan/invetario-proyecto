"""
Script para resetear la base de datos
ADVERTENCIA: Esto eliminará todas las tablas y datos existentes
"""
import pymysql

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Juanjesus200619',
    'database': 'inventario_tenis_padel'
}

def reset_database():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Conectado a la base de datos...")
        
        # Desactivar verificación de claves foráneas temporalmente
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Obtener todas las tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\nEliminando {len(tables)} tablas...")
            for table in tables:
                table_name = table[0]
                print(f"  - Eliminando tabla: {table_name}")
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        else:
            print("\nNo hay tablas para eliminar.")
        
        # Reactivar verificación de claves foráneas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        print("\nBase de datos reseteada exitosamente!")
        print("\nAhora puedes ejecutar: python run.py")
        print("Esto creara las tablas nuevas y el usuario administrador.")
        
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    print("=" * 60)
    print("RESETEAR BASE DE DATOS")
    print("=" * 60)
    print("\nADVERTENCIA: Esto eliminara TODAS las tablas y datos.")
    respuesta = input("\nEstas seguro de que deseas continuar? (si/no): ")
    
    if respuesta.lower() in ['si', 's', 'yes', 'y']:
        reset_database()
    else:
        print("\nOperacion cancelada.")
