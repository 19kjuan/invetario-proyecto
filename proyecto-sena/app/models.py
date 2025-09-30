from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    es_admin = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        if self.email == 'admin@inventario.com':
            self.es_admin = True
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, default=5, nullable=False)
    categoria = db.Column(db.Enum('Tenis', 'Pádel', 'Accesorios'), default='Accesorios')
    marca = db.Column(db.String(50))
    talla = db.Column(db.String(10))
    color = db.Column(db.String(30))
    imagen = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    movimientos = db.relationship('MovimientoInventario', backref='producto', lazy='dynamic')
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy='dynamic')
    
    def __repr__(self):
        return f'<Producto {self.codigo} - {self.nombre}>'
    
    def necesita_reponer(self):
        return self.stock <= self.stock_minimo

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ventas = db.relationship('Venta', backref='cliente', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'completada', 'cancelada'), default='pendiente')
    metodo_pago = db.Column(db.Enum('efectivo', 'tarjeta', 'transferencia'), nullable=False)
    notas = db.Column(db.Text)
    
    # Claves foráneas
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    
    # Relaciones
    detalles = db.relationship('DetalleVenta', backref='venta', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Venta {self.id} - {self.fecha}>'

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    descuento = db.Column(db.Numeric(10, 2), default=0)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Claves foráneas
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    def __repr__(self):
        return f'<DetalleVenta {self.id}>'

class MovimientoInventario(db.Model):
    __tablename__ = 'movimientos_inventario'
    
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste de inventario'),
        ('devolucion', 'Devolución')
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    tipo = db.Column(db.Enum(*[t[0] for t in TIPOS_MOVIMIENTO]), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    notas = db.Column(db.Text)
    
    # Claves foráneas
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'))
    
    def __repr__(self):
        return f'<MovimientoInventario {self.id} - {self.tipo} de {self.cantidad} unidades>'

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(200))
    descripcion = db.Column(db.String(200))
    
    @staticmethod
    def get_config(clave, valor_por_defecto=None):
        config = Configuracion.query.filter_by(clave=clave).first()
        return config.valor if config else valor_por_defecto
    
    @staticmethod
    def set_config(clave, valor, descripcion=''):
        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            config.valor = valor
        else:
            config = Configuracion(clave=clave, valor=valor, descripcion=descripcion)
            db.session.add(config)
        db.session.commit()
        return config
    
    def __repr__(self):
        return f'<Configuracion {self.clave}={self.valor}>'
