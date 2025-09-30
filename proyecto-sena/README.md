# Sistema de Gestión de Inventario - Tenis & Pádel

Aplicación web completa para gestionar el inventario de un emprendimiento de venta de artículos deportivos de tenis y pádel.

## Características Principales

### 1. Gestión de Productos
- ✅ Agregar nuevos productos con detalles completos (nombre, descripción, precio, categoría, etc.)
- ✅ Editar información de productos existentes
- ✅ Eliminar productos del inventario
- ✅ Actualizar precios y descripciones
- ✅ Subir imágenes de productos
- ✅ Búsqueda y filtrado por categoría

### 2. Control de Stock
- ✅ Visualización del stock disponible en tiempo real
- ✅ Alertas automáticas cuando el stock está bajo
- ✅ Ajuste manual de inventario con registro de movimientos
- ✅ Historial completo de movimientos de inventario

### 3. Módulo de Ventas
- ✅ Registrar ventas con actualización automática del stock
- ✅ Consultar historial de ventas por producto o período
- ✅ Anular ventas (solo administradores)
- ✅ Múltiples métodos de pago (efectivo, tarjeta, transferencia)
- ✅ Generación de informes de ventas

### 4. Dashboard y Reportes
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Productos más vendidos
- ✅ Ventas del día, semana y mes
- ✅ Valor total del inventario
- ✅ Productos con stock bajo

### 5. Seguridad
- ✅ Sistema de autenticación de usuarios
- ✅ Control de acceso por roles (administrador/usuario)
- ✅ Sesiones seguras

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, jQuery
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF, WTForms

## Estructura del Proyecto

```
proyecto-sena/
├── app/
│   ├── __init__.py           # Inicialización de la aplicación
│   ├── models.py             # Modelos de base de datos
│   ├── forms.py              # Formularios WTF
│   ├── routes/               # Rutas de la aplicación
│   │   ├── auth.py           # Autenticación
│   │   ├── productos.py      # Gestión de productos
│   │   ├── ventas.py         # Gestión de ventas
│   │   └── main.py           # Dashboard y páginas principales
│   ├── static/               # Archivos estáticos
│   │   └── uploads/          # Imágenes de productos
│   └── templates/            # Plantillas HTML
│       ├── base.html         # Plantilla base
│       ├── dashboard.html    # Dashboard principal
│       ├── auth/             # Templates de autenticación
│       ├── productos/        # Templates de productos
│       └── ventas/           # Templates de ventas
├── config.py                 # Configuración de la aplicación
├── run.py                    # Punto de entrada de la aplicación
├── reset_db.py               # Script para resetear la base de datos
└── requirements.txt          # Dependencias del proyecto
```

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el proyecto
El proyecto ya está en: `c:\Users\juanG\Music\invetario-proyecto\proyecto-sena`

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- Flask==3.1.2
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- Flask-WTF==1.2.1
- WTForms==3.1.2
- PyMySQL==1.1.2
- email-validator==2.1.0

### Paso 3: Configurar la base de datos
La aplicación está configurada para conectarse a:
- **Host**: localhost
- **Usuario**: root
- **Contraseña**: Juanjesus200619
- **Base de datos**: inventario_tenis_padel

Si necesitas cambiar estas credenciales, edita el archivo `config.py`.

### Paso 4: Inicializar la base de datos
La base de datos ya está creada y las tablas se generan automáticamente al iniciar la aplicación.

Si necesitas resetear la base de datos:
```bash
python reset_db.py
```

### Paso 5: Crear el usuario administrador
**IMPORTANTE**: Antes de poder iniciar sesión, debes crear el usuario administrador:
```bash
python crear_admin.py
```

Este comando creará el usuario con las credenciales por defecto.

### Paso 6: Ejecutar la aplicación
```bash
python run.py
```

La aplicación estará disponible en: **http://localhost:5000**

## Credenciales de Acceso

### Usuario Administrador por Defecto
- **Email**: admin@inventario.com
- **Contraseña**: admin123

**IMPORTANTE**: Cambia estas credenciales después del primer inicio de sesión.

## Uso de la Aplicación

### 1. Iniciar Sesión
1. Abre tu navegador y ve a `http://localhost:5000`
2. Ingresa las credenciales de administrador
3. Serás redirigido al dashboard principal

### 2. Agregar Productos
1. Ve a "Productos" en el menú lateral
2. Haz clic en "Agregar Producto"
3. Completa el formulario con los detalles del producto
4. Opcionalmente, sube una imagen
5. Haz clic en "Guardar Producto"

### 3. Registrar Ventas
1. Ve a "Ventas" en el menú lateral
2. Haz clic en "Nueva Venta"
3. Busca y agrega productos a la venta
4. Ajusta las cantidades según sea necesario
5. Selecciona el método de pago
6. Haz clic en "Registrar Venta"

### 4. Ajustar Inventario
1. Ve al detalle de un producto
2. Haz clic en "Ajustar Inventario"
3. Ingresa la cantidad (positiva para aumentar, negativa para disminuir)
4. Agrega notas explicativas
5. Confirma el ajuste

### 5. Ver Reportes
- El dashboard muestra estadísticas en tiempo real
- Accede a "Ventas" para ver el historial completo
- Filtra por fechas, métodos de pago o estado
- Ve "Stock Bajo" para productos que necesitan reposición

## Comandos Útiles

### Crear datos de ejemplo
```bash
flask --app run create-sample-data
```

### Resetear la base de datos
```bash
python reset_db.py
```

### Ejecutar en modo desarrollo
```bash
python run.py
```

### Ejecutar en modo producción
```bash
flask --app run run --host=0.0.0.0 --port=5000
```

## Modelos de Base de Datos

### Usuario
- Gestión de usuarios del sistema
- Roles: administrador y usuario estándar

### Producto
- Información completa del producto
- Control de stock y precios
- Categorización (Tenis, Pádel, Accesorios)

### Venta
- Registro de transacciones
- Estados: pendiente, completada, cancelada, anulada
- Métodos de pago múltiples

### DetalleVenta
- Productos incluidos en cada venta
- Cantidades y precios al momento de la venta

### MovimientoInventario
- Historial de todos los cambios en el inventario
- Tipos: entrada, salida, ajuste, devolución

### Cliente
- Información de clientes (opcional)
- Historial de compras

### Configuracion
- Parámetros configurables del sistema
- Umbrales de alertas

## Características de Seguridad

1. **Autenticación**: Sistema de login con sesiones seguras
2. **Autorización**: Control de acceso basado en roles
3. **Protección CSRF**: Tokens en todos los formularios
4. **Contraseñas**: Hash seguro con Werkzeug
5. **Validación**: Validación de datos en frontend y backend

## Personalización

### Cambiar el nombre del negocio
Edita el archivo `config.py` y modifica la configuración:
```python
Configuracion.set_config('nombre_negocio', 'Tu Nombre de Negocio', 'Nombre del negocio')
```

### Cambiar el umbral de stock bajo
```python
Configuracion.set_config('umbral_alerta_stock', '10', 'Umbral para alertas de stock bajo')
```

### Modificar estilos
Los estilos CSS están en el archivo `app/templates/base.html` dentro de la etiqueta `<style>`.

## Solución de Problemas

### Error de conexión a la base de datos
- Verifica que MySQL esté corriendo
- Confirma las credenciales en `config.py`
- Asegúrate de que la base de datos `inventario_tenis_padel` exista

### Error "tabla no existe"
Ejecuta:
```bash
python reset_db.py
python run.py
```

### Puerto 5000 en uso
Cambia el puerto en `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Próximas Mejoras

- [ ] Exportación de reportes a PDF/Excel
- [ ] Gráficos interactivos de ventas
- [ ] Sistema de notificaciones por email
- [ ] Gestión de proveedores
- [ ] Códigos de barras
- [ ] Aplicación móvil

## Soporte

Para preguntas o problemas, contacta al desarrollador o consulta la documentación de Flask:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)

## Licencia

Este proyecto es de uso privado para el emprendimiento de Tenis & Pádel.

---

**Desarrollado con ❤️ para la gestión eficiente de tu inventario**
