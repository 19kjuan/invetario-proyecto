from flask import Blueprint, render_template, request
from flask_login import login_required
from datetime import datetime, timedelta, date
from sqlalchemy import func
from app import db
from app.models import Producto, Venta, DetalleVenta

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes/ventas')
@login_required
def reporte_ventas():
    """Reporte detallado de ventas por período"""
    # Valores por defecto (último mes)
    hoy = date.today()
    periodo_inicio = request.args.get('inicio', (hoy.replace(day=1) - timedelta(days=30)).strftime('%Y-%m-%d'))
    periodo_fin = request.args.get('fin', hoy.strftime('%Y-%m-%d'))

    try:
        inicio_dt = datetime.strptime(periodo_inicio, '%Y-%m-%d').date()
        fin_dt = datetime.strptime(periodo_fin, '%Y-%m-%d').date()
    except ValueError:
        inicio_dt = hoy.replace(day=1) - timedelta(days=30)
        fin_dt = hoy

    # Resumen general
    resumen = db.session.query(
        func.count(Venta.id).label('total_ventas'),
        func.sum(Venta.total).label('ingresos_totales'),
        func.avg(Venta.total).label('ticket_promedio')
    ).filter(
        Venta.fecha.between(inicio_dt, fin_dt + timedelta(days=1))
    ).first()

    # Productos más vendidos por cantidad
    top_cantidad = db.session.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label('cantidad_total')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha.between(inicio_dt, fin_dt + timedelta(days=1))
    ).group_by(
        Producto.id, Producto.nombre
    ).order_by(
        func.sum(DetalleVenta.cantidad).desc()
    ).limit(10).all()

    # Productos con mayores ingresos
    top_ingresos = db.session.query(
        Producto.nombre,
        func.sum(DetalleVenta.subtotal).label('ingresos_totales')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha.between(inicio_dt, fin_dt + timedelta(days=1))
    ).group_by(
        Producto.id, Producto.nombre
    ).order_by(
        func.sum(DetalleVenta.subtotal).desc()
    ).limit(10).all()

    # Ventas por día (para gráfico)
    ventas_diarias = db.session.query(
        func.date(Venta.fecha).label('fecha'),
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        Venta.fecha.between(inicio_dt, fin_dt + timedelta(days=1))
    ).group_by(
        func.date(Venta.fecha)
    ).order_by(
        'fecha'
    ).all()
    
    # Convertir fechas a strings para el template
    ventas_diarias = [
        {
            'fecha': v.fecha.strftime('%Y-%m-%d') if v.fecha else '',
            'cantidad': v.cantidad or 0,
            'total': float(v.total) if v.total else 0
        }
        for v in ventas_diarias
    ]

    return render_template('reportes/ventas.html',
                         title='Reporte de Ventas',
                         resumen=resumen,
                         top_cantidad=top_cantidad,
                         top_ingresos=top_ingresos,
                         ventas_diarias=ventas_diarias,
                         periodo_inicio=inicio_dt,
                         periodo_fin=fin_dt)
