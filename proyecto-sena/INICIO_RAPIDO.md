# Guía de Inicio Rápido

## ¡Tu aplicación está lista! 🎉

La aplicación de gestión de inventario está completamente configurada y funcionando.

## Acceso Inmediato

### 1. La aplicación ya está corriendo
- **URL**: http://localhost:5000
- **Estado**: ✅ Activo

### 2. Crear usuario administrador (IMPORTANTE)
Si es la primera vez que usas la aplicación, ejecuta:
```bash
python crear_admin.py
```

### 3. Credenciales de acceso
```
Email: admin@inventario.com
Contraseña: admin123
```

## Primeros Pasos

### Paso 1: Iniciar sesión
1. Abre tu navegador
2. Ve a: http://localhost:5000
3. Ingresa las credenciales de administrador
4. ¡Listo! Estás en el dashboard

### Paso 2: Agregar tu primer producto
1. Haz clic en "Productos" en el menú lateral
2. Clic en "Agregar Producto"
3. Completa la información:
   - Código (ej: RAQ-001)
   - Nombre (ej: Raqueta Wilson Pro)
   - Precio de compra y venta
   - Stock inicial
   - Categoría (Tenis, Pádel o Accesorios)
4. Guarda el producto

### Paso 3: Registrar tu primera venta
1. Ve a "Ventas" → "Nueva Venta"
2. Busca el producto que agregaste
3. Selecciona la cantidad
4. Elige el método de pago
5. Registra la venta

## Comandos Importantes

### Iniciar la aplicación (si se detuvo)
```bash
cd c:\Users\juanG\Music\invetario-proyecto\proyecto-sena
python run.py
```

### Detener la aplicación
Presiona `Ctrl + C` en la terminal donde está corriendo

### Resetear la base de datos (elimina todos los datos)
```bash
python reset_db.py
```

### Crear datos de ejemplo para pruebas
```bash
flask --app run create-sample-data
```

## Funcionalidades Principales

### 📦 Gestión de Productos
- **Agregar**: Productos → Agregar Producto
- **Editar**: Clic en el ícono de lápiz
- **Ver detalles**: Clic en el ícono de ojo
- **Ajustar stock**: Desde el detalle del producto

### 💰 Gestión de Ventas
- **Nueva venta**: Ventas → Nueva Venta
- **Ver historial**: Ventas → Lista de Ventas
- **Ver detalles**: Clic en el ícono de ojo
- **Anular venta**: Desde el detalle (solo admin)

### 📊 Dashboard
- **Ventas del día**: Resumen en tiempo real
- **Stock bajo**: Productos que necesitan reposición
- **Productos más vendidos**: Top 5 del mes
- **Acceso rápido**: Botones para acciones comunes

### ⚠️ Alertas de Stock
- **Ver productos con stock bajo**: Stock Bajo en el menú
- **Configurar umbral**: Por defecto es 5 unidades

## Estructura del Menú

```
📊 Dashboard          → Resumen general
📦 Productos          → Gestión de inventario
💰 Ventas             → Registro y consulta de ventas
⚠️  Stock Bajo        → Productos que necesitan reposición
📈 Reportes           → Estadísticas y análisis
👥 Usuarios           → Gestión de usuarios (solo admin)
⚙️  Configuración     → Ajustes del sistema (solo admin)
👤 Mi Perfil          → Datos del usuario
🚪 Cerrar Sesión      → Salir de la aplicación
```

## Categorías de Productos

La aplicación soporta 3 categorías:
1. **Tenis** - Raquetas, zapatillas, ropa de tenis
2. **Pádel** - Palas, pelotas, accesorios de pádel
3. **Accesorios** - Bolsos, grips, muñequeras, etc.

## Métodos de Pago

- **Efectivo** - Pago en efectivo
- **Tarjeta** - Tarjeta de crédito/débito
- **Transferencia** - Transferencia bancaria

## Tips y Recomendaciones

### ✅ Buenas Prácticas
1. **Códigos únicos**: Usa códigos descriptivos (ej: RAQ-001, PEL-001)
2. **Stock mínimo**: Configura alertas para cada producto
3. **Imágenes**: Sube fotos de los productos para mejor visualización
4. **Notas en ventas**: Agrega notas para referencia futura
5. **Backup regular**: Respalda tu base de datos periódicamente

### ⚡ Atajos Rápidos
- **Dashboard**: Botones de acceso rápido en la parte inferior
- **Búsqueda**: Usa la barra de búsqueda en productos
- **Filtros**: Filtra por categoría, fecha, método de pago
- **Paginación**: Navega entre páginas si tienes muchos registros

### 🔒 Seguridad
1. **Cambia la contraseña**: Actualiza la contraseña del admin
2. **Crea usuarios**: Agrega usuarios con permisos limitados si es necesario
3. **Cierra sesión**: Siempre cierra sesión al terminar

## Solución Rápida de Problemas

### ❌ No puedo acceder a la aplicación
```bash
# Verifica que el servidor esté corriendo
# Si no, ejecuta:
python run.py
```

### ❌ Error de base de datos
```bash
# Resetea la base de datos
python reset_db.py
# Luego inicia la aplicación
python run.py
```

### ❌ Olvidé la contraseña
```bash
# Resetea la base de datos (perderás los datos)
python reset_db.py
# O contacta al desarrollador para recuperarla
```

## Próximos Pasos

1. ✅ Cambiar la contraseña del administrador
2. ✅ Agregar tus productos reales
3. ✅ Configurar los stocks mínimos
4. ✅ Comenzar a registrar ventas
5. ✅ Revisar el dashboard diariamente

## Contacto y Soporte

Si necesitas ayuda o tienes preguntas:
- Consulta el archivo `README.md` para documentación completa
- Revisa los logs en la terminal donde corre la aplicación
- Contacta al desarrollador

---

**¡Disfruta gestionando tu inventario de manera eficiente!** 🚀
