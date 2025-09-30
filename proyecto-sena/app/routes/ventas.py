from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, extract, and_, or_
from app import db
from app.models import (
    Venta, DetalleVenta, Producto, Cliente, MovimientoInventario, Usuario, Configuracion
)
from app.forms import VentaForm, ClienteForm, FiltroVentasForm
import json

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/')
@login_required
def listar():
    page = request.args.get('page', 1, type=int)
    form = FiltroVentasForm()
    
    # Configurar valores predeterminados para el formulario
    hoy = datetime.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener fechas del formulario o usar valores por defecto (mes actual)
    fecha_inicio = request.args.get('fecha_inicio', inicio_mes.strftime('%Y-%m-%d'))
    fecha_fin = request.args.get('fecha_fin', hoy.strftime('%Y-%m-%d'))
    
    # Convertir a objetos de fecha para la consulta
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)  # Incluir todo el día
    except (ValueError, TypeError):
        fecha_inicio_dt = inicio_mes
        fecha_fin_dt = hoy + timedelta(days=1)
    
    # Construir la consulta base
    query = Venta.query.filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt)
    )
    
    # Aplicar filtros adicionales si se proporcionan
    if 'estado' in request.args and request.args['estado']:
        query = query.filter(Venta.estado == request.args['estado'])
    
    if 'metodo_pago' in request.args and request.args['metodo_pago']:
        query = query.filter(Venta.metodo_pago == request.args['metodo_pago'])
    
    if 'cliente_id' in request.args and request.args['cliente_id']:
        query = query.filter(Venta.cliente_id == request.args['cliente_id'])
    
    # Ordenar por fecha más reciente primero
    ventas = query.order_by(Venta.fecha.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_POR_PAGINA'], error_out=False)
    
    # Calcular totales
    total_ventas = db.session.query(func.sum(Venta.total)).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).scalar() or 0
    
    total_ventas = float(total_ventas)
    
    # Obtener estadísticas por categoría
    stats_categorias = db.session.query(
        Producto.categoria,
        func.sum(DetalleVenta.cantidad).label('cantidad'),
        func.sum(DetalleVenta.subtotal).label('total')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).group_by(
        Producto.categoria
    ).all()
    
    # Obtener los 5 productos más vendidos
    productos_mas_vendidos = db.session.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label('cantidad'),
        func.sum(DetalleVenta.subtotal).label('total')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).group_by(
        Producto.id, Producto.nombre
    ).order_by(
        func.sum(DetalleVenta.cantidad).desc()
    ).limit(5).all()
    
    # Pasar los filtros al template
    filtros = {
        'fecha_inicio': fecha_inicio_dt.strftime('%Y-%m-%d'),
        'fecha_fin': (fecha_fin_dt - timedelta(days=1)).strftime('%Y-%m-%d'),
        'estado': request.args.get('estado', ''),
        'metodo_pago': request.args.get('metodo_pago', ''),
        'cliente_id': request.args.get('cliente_id', '')
    }
    
    return render_template('ventas/listar.html',
                         title='Ventas',
                         ventas=ventas,
                         total_ventas=total_ventas,
                         stats_categorias=stats_categorias,
                         productos_mas_vendidos=productos_mas_vendidos,
                         filtros=filtros,
                         form=form)

@ventas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form = VentaForm()
    
    # Cargar clientes para el select
    clientes = [(str(c.id), f"{c.nombre} {c.apellido or ''}".strip()) for c in Cliente.query.order_by(Cliente.nombre).all()]
    form.cliente_id.choices = [('', 'Seleccione un cliente...')] + clientes
    
    if form.validate_on_submit():
        try:
            # Crear la venta
            venta = Venta(
                total=0,  # Se calculará con los detalles
                estado='pendiente',
                metodo_pago=form.metodo_pago.data,
                notas=form.notas.data,
                usuario_id=current_user.id,
                cliente_id=form.cliente_id.data or None
            )
            
            db.session.add(venta)
            db.session.flush()  # Para obtener el ID de la venta
            
            # Procesar los detalles de la venta
            total_venta = 0
            detalles = json.loads(form.detalles_venta.data)
            
            for detalle in detalles:
                producto = Producto.query.get(detalle['producto_id'])
                if not producto:
                    continue
                
                cantidad = int(detalle['cantidad'])
                precio_unitario = float(detalle['precio_unitario'])
                subtotal = cantidad * precio_unitario
                
                # Crear el detalle de la venta
                detalle_venta = DetalleVenta(
                    venta_id=venta.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                
                db.session.add(detalle_venta)
                total_venta += subtotal
                
                # Actualizar el stock del producto
                producto.stock -= cantidad
                
                # Registrar el movimiento de inventario
                movimiento = MovimientoInventario(
                    tipo='salida',
                    cantidad=cantidad,
                    notas=f'Venta #{venta.id}',
                    producto_id=producto.id,
                    usuario_id=current_user.id,
                    venta_id=venta.id
                )
                db.session.add(movimiento)
            
            # Actualizar el total de la venta
            venta.total = total_venta
            venta.estado = 'completada'
            
            db.session.commit()
            
            flash('Venta registrada exitosamente!', 'success')
            return redirect(url_for('ventas.detalle', id=venta.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar la venta: {str(e)}')
            flash('Ocurrió un error al registrar la venta. Por favor, inténtalo de nuevo.', 'danger')
    
    return render_template('ventas/nueva.html',
                         title='Nueva Venta',
                         form=form)

@ventas_bp.route('/<int:id>')
@login_required
def detalle(id):
    venta = Venta.query.get_or_404(id)
    return render_template('ventas/detalle.html',
                         title=f'Venta #{venta.id}',
                         venta=venta)

@ventas_bp.route('/anular/<int:id>', methods=['POST'])
@login_required
def anular(id):
    venta = Venta.query.get_or_404(id)
    
    # Solo se pueden anular ventas pendientes o completadas
    if venta.estado not in ['pendiente', 'completada']:
        flash('No se puede anular una venta que ya ha sido anulada o cancelada.', 'warning')
        return redirect(url_for('ventas.detalle', id=id))
    
    try:
        # Revertir el stock de los productos
        for detalle in venta.detalles:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            
            # Registrar el movimiento de inventario
            movimiento = MovimientoInventario(
                tipo='devolucion',
                cantidad=detalle.cantidad,
                notas=f'Anulación de venta #{venta.id}',
                producto_id=producto.id,
                usuario_id=current_user.id,
                venta_id=venta.id
            )
            db.session.add(movimiento)
        
        # Marcar la venta como anulada
        venta.estado = 'anulada'
        venta.notas = f"Anulada por {current_user.nombre_usuario} - {request.form.get('motivo', 'Sin motivo especificado')}"
        
        db.session.commit()
        
        flash('Venta anulada exitosamente. El stock ha sido actualizado.', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al anular la venta: {str(e)}')
        flash('Ocurrió un error al anular la venta. Por favor, inténtalo de nuevo.', 'danger')
    
    return redirect(url_for('ventas.detalle', id=id))

@ventas_bp.route('/api/clientes')
@login_required
def api_clientes():
    """API para autocompletado de clientes"""
    search = request.args.get('q', '')
    
    query = Cliente.query.filter(
        or_(
            Cliente.nombre.ilike(f'%{search}%'),
            Cliente.apellido.ilike(f'%{search}%'),
            Cliente.email.ilike(f'%{search}%')
        )
    ).limit(10)
    
    clientes = [{
        'id': c.id,
        'nombre': f"{c.nombre} {c.apellido or ''}".strip(),
        'email': c.email or '',
        'telefono': c.telefono or ''
    } for c in query]
    
    return jsonify(clientes)

@ventas_bp.route('/api/ventas/estadisticas')
@login_required
def api_estadisticas():
    """API para obtener estadísticas de ventas"""
    # Obtener parámetros de fecha (últimos 30 días por defecto)
    hoy = datetime.now().date()
    fecha_inicio = request.args.get('fecha_inicio', (hoy - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.args.get('fecha_fin', hoy.strftime('%Y-%m-%d'))
    
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)  # Incluir todo el día
    except (ValueError, TypeError):
        fecha_inicio_dt = hoy - timedelta(days=30)
        fecha_fin_dt = hoy + timedelta(days=1)
    
    # Ventas por día
    ventas_por_dia = db.session.query(
        func.date(Venta.fecha).label('fecha'),
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).group_by(
        func.date(Venta.fecha)
    ).order_by(
        'fecha'
    ).all()
    
    # Ventas por categoría
    ventas_por_categoria = db.session.query(
        Producto.categoria,
        func.sum(DetalleVenta.cantidad).label('cantidad'),
        func.sum(DetalleVenta.subtotal).label('total')
    ).join(
        DetalleVenta, DetalleVenta.producto_id == Producto.id
    ).join(
        Venta, Venta.id == DetalleVenta.venta_id
    ).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).group_by(
        Producto.categoria
    ).all()
    
    # Métodos de pago
    metodos_pago = db.session.query(
        Venta.metodo_pago,
        func.count(Venta.id).label('cantidad'),
        func.sum(Venta.total).label('total')
    ).filter(
        Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
        Venta.estado == 'completada'
    ).group_by(
        Venta.metodo_pago
    ).all()
    
    # Preparar datos para la respuesta
    datos = {
        'ventas_por_dia': [{
            'fecha': v.fecha.strftime('%Y-%m-%d'),
            'cantidad': v.cantidad or 0,
            'total': float(v.total) if v.total else 0
        } for v in ventas_por_dia],
        
        'ventas_por_categoria': [{
            'categoria': v.categoria,
            'cantidad': v.cantidad or 0,
            'total': float(v.total) if v.total else 0
        } for v in ventas_por_categoria],
        
        'metodos_pago': [{
            'metodo': v.metodo_pago,
            'cantidad': v.cantidad or 0,
            'total': float(v.total) if v.total else 0
        } for v in metodos_pago],
        
        'resumen': {
            'total_ventas': float(db.session.query(func.sum(Venta.total)).filter(
                Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
                Venta.estado == 'completada'
            ).scalar() or 0),
            
            'total_ventas_count': db.session.query(func.count(Venta.id)).filter(
                Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
                Venta.estado == 'completada'
            ).scalar() or 0,
            
            'ticket_promedio': float(db.session.query(
                func.avg(Venta.total)
            ).filter(
                Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt),
                Venta.estado == 'completada'
            ).scalar() or 0)
        }
    }
    
    return jsonify(datos)
