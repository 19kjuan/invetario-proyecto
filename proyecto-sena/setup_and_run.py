#!/usr/bin/env python3
"""
Script para configurar y ejecutar la aplicación de inventario deportivo
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*50}")
    print(f"Ejecutando: {description}")
    print(f"Comando: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Comando ejecutado exitosamente")
        if result.stdout:
            print("Salida:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        if e.stderr:
            print("Error:", e.stderr)
        return False

def main():
    print("Configurando aplicacion de inventario deportivo...")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app"):
        print("Error: No se encontro el directorio 'app'")
        print("Asegurate de ejecutar este script desde el directorio del proyecto")
        return False
    
    # 1. Instalar dependencias
    if not run_command("pip install -r requeriments.txt", "Instalando dependencias de Python"):
        print("Error al instalar dependencias")
        return False
    
    # 2. Ejecutar el script SQL para crear la base de datos
    print("\nConfigurando base de datos...")
    print("IMPORTANTE: Asegurate de que MySQL este ejecutandose y que tengas acceso con:")
    print("Usuario: root")
    print("Contrasena: Juanjesus200619")
    print("Base de datos: inventario_deportivo")
    
    # Crear la base de datos usando MySQL
    mysql_command = """
    mysql -u root -pJuanjesus200619 -e "DROP DATABASE IF EXISTS inventario_deportivo; CREATE DATABASE inventario_deportivo;"
    """
    
    if not run_command(mysql_command, "Creando base de datos"):
        print("Error al crear la base de datos")
        print("Verifica que MySQL este ejecutandose y las credenciales sean correctas")
        return False
    
    # Ejecutar el script SQL
    sql_command = "mysql -u root -pJuanjesus200619 inventario_deportivo < setup_database.sql"
    if not run_command(sql_command, "Ejecutando script SQL"):
        print("Error al ejecutar el script SQL")
        return False
    
    # 3. Inicializar la base de datos con Flask
    if not run_command("python -c \"from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Base de datos inicializada')\"", "Inicializando base de datos con Flask"):
        print("Error al inicializar la base de datos con Flask")
        return False
    
    # 4. Crear usuario administrador
    if not run_command("python crear_admin.py", "Creando usuario administrador"):
        print("Error al crear usuario administrador")
        return False
    
    # 5. Crear datos de ejemplo
    if not run_command("python -c \"from run import app; app.app_context().push(); from run import create_sample_data; create_sample_data()\"", "Creando datos de ejemplo"):
        print("Error al crear datos de ejemplo")
        return False
    
    print("\nConfiguracion completada exitosamente!")
    print("\nResumen de la configuracion:")
    print("- Dependencias instaladas")
    print("- Base de datos creada: inventario_deportivo")
    print("- Tablas creadas con datos de ejemplo")
    print("- Usuario administrador creado")
    print("- Datos de ejemplo cargados")
    
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
        sys.exit(1)
    else:
        print("\nConfiguracion exitosa! Puedes ejecutar la aplicacion ahora.")
