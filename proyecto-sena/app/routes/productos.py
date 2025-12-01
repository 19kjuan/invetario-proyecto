from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import Producto, Configuracion
from app.forms import ProductoForm, AjusteInventarioForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename

productos_bp = Blueprint('productos', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@productos_bp.route('/')
@login_required
def listar():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    
    query = Producto.query
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Producto.nombre.like(search),
                Producto.descripcion.like(search)
            )
        )
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    productos = query.order_by(Producto.nombre).paginate(
        page=page, per_page=current_app.config['ITEMS_POR_PAGINA'], error_out=False)
    
    return render_template('productos/listar.html', 
                         title='Productos', 
                         productos=productos,
                         search=search,
                         categoria=categoria)

@productos_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    form = ProductoForm()
    
    if form.validate_on_submit():
        # Manejar la carga de la imagen
        imagen_nombre = None
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                # Guardar con un nombre único basado en la fecha y hora
                nombre_base, extension = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{nombre_base}_{timestamp}{extension}"
                
                # Crear directorio de uploads si no existe
                upload_folder = os.path.join(current_app.root_path, 'static/uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Guardar el archivo
                archivo.save(os.path.join(upload_folder, filename))
                imagen_nombre = filename
        
        # Crear el producto (guardar imagen si se cargó)
        producto = Producto(
            codigo=form.codigo.data,
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio_compra=form.precio_compra.data,
            precio_venta=form.precio_venta.data,
            stock=form.stock_inicial.data,
            stock_minimo=form.stock_minimo.data,
            categoria=form.categoria.data,
            marca=form.marca.data,
            talla=form.talla.data,
            color=form.color.data,
            imagen=imagen_nombre,
            activo=True
        )
        
        db.session.add(producto)
        
        db.session.commit()
        
        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('productos.detalle', id=producto.id))
    
    return render_template('productos/agregar.html', 
                         title='Agregar Producto', 
                         form=form)

@productos_bp.route('/<int:id>')
@login_required
def detalle(id):
    producto = Producto.query.get_or_404(id)
    
    return render_template('productos/detalle.html', 
                         title=producto.nombre, 
                         producto=producto)

@productos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    
    if form.validate_on_submit():
        # Manejar la carga de la imagen
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo and allowed_file(archivo.filename):
                # Eliminar la imagen anterior si existe
                if producto.imagen:
                    try:
                        os.remove(os.path.join(
                            current_app.root_path, 
                            'static/uploads', 
                            producto.imagen
                        ))
                    except OSError:
                        pass
                
                # Guardar la nueva imagen
                filename = secure_filename(archivo.filename)
                nombre_base, extension = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{nombre_base}_{timestamp}{extension}"
                
                upload_folder = os.path.join(current_app.root_path, 'static/uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                archivo.save(os.path.join(upload_folder, filename))
                producto.imagen = filename
        
        # Actualizar los demás campos
        producto.codigo = form.codigo.data
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.precio_compra = form.precio_compra.data
        producto.precio_venta = form.precio_venta.data
        producto.stock = form.stock_inicial.data if form.stock_inicial.data is not None else producto.stock
        producto.stock_minimo = form.stock_minimo.data
        producto.categoria = form.categoria.data
        producto.marca = form.marca.data
        producto.talla = form.talla.data
        producto.color = form.color.data
        
        db.session.commit()
        
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos.detalle', id=producto.id))
    
    return render_template('productos/editar.html', 
                         title='Editar Producto', 
                         form=form, 
                         producto=producto)

@productos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if not current_user.es_admin:
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('productos.listar'))
    
    producto = Producto.query.get_or_404(id)
    
    # Eliminar la imagen si existe
    if producto.imagen:
        try:
            os.remove(os.path.join(
                current_app.root_path, 
                'static/uploads', 
                producto.imagen
            ))
        except OSError:
            pass
    
    db.session.delete(producto)
    db.session.commit()
    
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos.listar'))


@productos_bp.route('/bajo-stock')
@login_required
def bajo_stock():
    page = request.args.get('page', 1, type=int)
    
    # Obtener el umbral de stock mínimo (puede configurarse en la base de datos)
    umbral = Configuracion.get_config('umbral_alerta_stock', '5')
    try:
        umbral = int(umbral)
    except (ValueError, TypeError):
        umbral = 5
    
    # Filtrar productos con stock menor o igual al umbral
    productos = Producto.query.filter(
        Producto.stock <= umbral
    ).order_by(
        Producto.stock.asc()
    ).paginate(
        page=page, 
        per_page=current_app.config['ITEMS_POR_PAGINA'], 
        error_out=False
    )
    
    return render_template('productos/bajo_stock.html',
                         title='Productos con Bajo Stock',
                         productos=productos,
                         umbral=umbral)

@productos_bp.route('/api/productos')
@login_required
def api_productos():
    """API para autocompletado en formularios de ventas"""
    search = request.args.get('q', '')
    
    query = Producto.query.filter(
        or_(
            Producto.nombre.ilike(f'%{search}%')
        )
    ).limit(10)
    
    productos = [{
        'id': p.id,
        'codigo': p.codigo,
        'nombre': p.nombre,
        'precio': float(p.precio_venta) if p.precio_venta else 0,
        'stock': p.stock,
        'imagen': p.imagen
    } for p in query]
    
    return jsonify(productos)
