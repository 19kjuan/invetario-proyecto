# Sistema de Inventario Deportivo - Court-Side Tennis Club

## 🎯 Descripción
Sistema de gestión de inventario especializado en productos deportivos de tenis y pádel, desarrollado con Flask y MySQL.

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

### Configuración Automática
```bash
# 1. Ejecutar el script de configuración automática
python setup_and_run.py
```

### Configuración Manual
```bash
# 1. Instalar dependencias
pip install -r requeriments.txt

# 2. Configurar base de datos MySQL
mysql -u root -p
# Ejecutar el script setup_database.sql

# 3. Inicializar la aplicación
python run.py
```

## 🗄️ Estructura de Base de Datos

### Tablas Principales
- **productos**: Información de productos deportivos
- **ventas**: Registro de ventas
- **detalle_ventas**: Detalles de productos vendidos
- **usuarios**: Usuarios del sistema
- **configuraciones**: Configuraciones del sistema

### Características de la Base de Datos
- ✅ Trigger automático para actualizar stock al realizar ventas
- ✅ Datos de ejemplo pre-cargados
- ✅ Estructura optimizada para inventario deportivo

## 🔧 Configuración

### Base de Datos
- **Host**: localhost
- **Puerto**: 3306
- **Usuario**: root
- **Contraseña**: Juanjesus200619
- **Base de datos**: inventario_deportivo

### Usuario Administrador
- **Email**: admin@inventario.com
- **Contraseña**: admin123

## 📊 Funcionalidades

### Gestión de Productos
- ✅ Listado y búsqueda de productos
- ✅ Agregar nuevos productos
- ✅ Editar productos existentes
- ✅ Control de stock automático
- ✅ Alertas de stock bajo

### Gestión de Ventas
- ✅ Registro de nuevas ventas
- ✅ Listado de ventas con filtros
- ✅ Detalle de ventas
- ✅ Actualización automática de stock

### Dashboard
- ✅ Estadísticas de ventas
- ✅ Productos más vendidos
- ✅ Alertas de stock bajo
- ✅ Resumen de inventario

## 🎨 Interfaz de Usuario

### Páginas Principales
- **Landing Page**: Página de bienvenida
- **Dashboard**: Panel principal con estadísticas
- **Productos**: Gestión completa de productos
- **Ventas**: Gestión de ventas
- **Reportes**: Análisis y reportes
- **Configuración**: Configuración del sistema

### Características de la UI
- ✅ Diseño responsivo
- ✅ Interfaz moderna y limpia
- ✅ Navegación intuitiva
- ✅ Formularios validados

## 🔒 Seguridad

### Autenticación
- ✅ Sistema de login seguro
- ✅ Contraseñas encriptadas
- ✅ Sesiones de usuario
- ✅ Control de acceso por roles

### Validaciones
- ✅ Validación de formularios
- ✅ Sanitización de datos
- ✅ Protección contra inyección SQL

## 📈 Monitoreo y Reportes

### Estadísticas Disponibles
- Ventas por período (día, semana, mes)
- Productos más vendidos
- Ventas por categoría
- Valor total del inventario
- Productos con bajo stock

### Reportes
- Reportes de ventas
- Análisis de inventario
- Estadísticas de productos

## 🛠️ Desarrollo

### Estructura del Proyecto
```
proyecto-sena/
├── app/
│   ├── routes/          # Rutas de la aplicación
│   ├── templates/       # Plantillas HTML
│   ├── static/          # Archivos estáticos
│   └── models.py        # Modelos de base de datos
├── config.py            # Configuración
├── run.py              # Punto de entrada
└── setup_database.sql  # Script de base de datos
```

### Tecnologías Utilizadas
- **Backend**: Flask, SQLAlchemy
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF

## 🚀 Ejecución

### Modo Desarrollo
```bash
python run.py
```

### Acceso a la Aplicación
- **URL**: http://localhost:5000
- **Usuario**: admin@inventario.com
- **Contraseña**: admin123

## 📝 Notas Importantes

### Cambios Realizados
1. ✅ Actualizada la estructura de base de datos según especificaciones
2. ✅ Simplificados los modelos para coincidir con el esquema SQL
3. ✅ Actualizadas todas las rutas para funcionar con el nuevo esquema
4. ✅ Eliminadas funcionalidades no requeridas (clientes, movimientos de inventario)
5. ✅ Configurada la conexión a la base de datos con credenciales especificadas

### Datos de Ejemplo
El sistema incluye productos de ejemplo:
- Raquetas de tenis y pádel
- Pelotas deportivas
- Accesorios (grips, bolsos)
- Precios y stock configurados

## 🔧 Solución de Problemas

### Error de Conexión a Base de Datos
1. Verificar que MySQL esté ejecutándose
2. Confirmar credenciales de acceso
3. Verificar que la base de datos existe

### Error de Dependencias
1. Ejecutar: `pip install -r requeriments.txt`
2. Verificar versión de Python (3.8+)

### Error de Permisos
1. Verificar permisos de escritura en directorio
2. Ejecutar con permisos de administrador si es necesario

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema, contactar al equipo de desarrollo.

---

**Desarrollado para Court-Side Tennis Club** 🎾
