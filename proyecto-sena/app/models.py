from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
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
    
    # Usar atributo moderno `id` mapeado a la columna real `productos.id`
    id = db.Column('id', db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False, default=5)
    categoria = db.Column(db.Enum('Tenis', 'Pádel', 'Accesorios'))
    marca = db.Column(db.String(50))
    talla = db.Column(db.String(10))
    color = db.Column(db.String(30))
    imagen = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy='dynamic')
    
    def __repr__(self):
        return f'<Producto {self.id} - {self.nombre}>'


class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'completada', 'cancelada', 'anulada'))
    metodo_pago = db.Column(db.Enum('efectivo', 'tarjeta', 'transferencia'))
    notas = db.Column(db.Text)
    usuario_id = db.Column(db.Integer)
    cliente_id = db.Column(db.Integer)
    
    # Relaciones
    detalles = db.relationship('DetalleVenta', backref='venta', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Venta {self.id} - {self.fecha}>'

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    # Mapear a columnas existentes en BD usando nombres de atributo modernos
    venta_id = db.Column('venta_id', db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<DetalleVenta {self.id}>'


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
