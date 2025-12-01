from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_
from app import db
from app.models import Producto, Venta, DetalleVenta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page principal"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html', title='Court-Side Tennis Club')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal con estadísticas y resumen"""
    
    # Obtener fechas para estadísticas
    hoy = datetime.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    
    # Estadísticas de ventas del mes
    ventas_mes = db.session.query(
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        Venta.fecha >= inicio_mes
    ).first()
    
    # Estadísticas de ventas de la semana
    ventas_semana = db.session.query(
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        Venta.fecha >= inicio_semana
    ).first()
    
    # Estadísticas de ventas de hoy
    ventas_hoy = db.session.query(
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        func.date(Venta.fecha) == hoy
    ).first()
    
    # Productos con bajo stock
    productos_bajo_stock = Producto.query.filter(
        Producto.stock <= 5
    ).order_by(Producto.stock.asc()).limit(10).all()
    
    # Productos más vendidos del mes
    productos_mas_vendidos = db.session.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label('cantidad_vendida'),
        func.sum(DetalleVenta.subtotal).label('total_vendido')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha >= inicio_mes
    ).group_by(
        Producto.id, Producto.nombre
    ).order_by(
        func.sum(DetalleVenta.cantidad).desc()
    ).limit(5).all()
    
    # Últimas ventas
    ultimas_ventas = Venta.query.order_by(
        Venta.fecha.desc()
    ).limit(5).all()
    
    # Estadísticas de productos
    total_productos = Producto.query.count()
    valor_inventario = db.session.query(
        func.sum(Producto.stock * Producto.precio_venta)
    ).scalar() or 0
    
    # Ventas por categoría del mes
    ventas_por_categoria = db.session.query(
        Producto.categoria,
        func.sum(DetalleVenta.cantidad).label('cantidad'),
        func.sum(DetalleVenta.subtotal).label('total')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha >= inicio_mes
    ).group_by(
        Producto.categoria
    ).all()
    
    # Preparar datos para el template
    estadisticas = {
        'ventas_mes': {
            'cantidad': ventas_mes.cantidad or 0,
            'total': float(ventas_mes.total) if ventas_mes.total else 0
        },
        'ventas_semana': {
            'cantidad': ventas_semana.cantidad or 0,
            'total': float(ventas_semana.total) if ventas_semana.total else 0
        },
        'ventas_hoy': {
            'cantidad': ventas_hoy.cantidad or 0,
            'total': float(ventas_hoy.total) if ventas_hoy.total else 0
        },
        'total_productos': total_productos,
        'valor_inventario': float(valor_inventario),
        'productos_bajo_stock_count': len(productos_bajo_stock)
    }
    
    return render_template('dashboard.html',
                         title='Dashboard',
                         estadisticas=estadisticas,
                         productos_bajo_stock=productos_bajo_stock,
                         productos_mas_vendidos=productos_mas_vendidos,
                         ultimas_ventas=ultimas_ventas,
                         ventas_por_categoria=ventas_por_categoria)

@main_bp.route('/reportes')
@login_required
def reportes():
    """Página de reportes"""
    return render_template('reportes.html', title='Reportes')

@main_bp.route('/configuracion')
@login_required
def configuracion():
    """Página de configuración"""
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Obtener estadísticas del sistema
    from app.models import Usuario
    
    stats = {
        'total_productos': Producto.query.count(),
        'total_ventas': Venta.query.count(),
        'total_usuarios': Usuario.query.filter(Usuario.activo == True).count()
    }
    
    return render_template('configuracion.html', title='Configuración', stats=stats)
