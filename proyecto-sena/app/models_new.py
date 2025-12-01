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
    
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    categoria = db.Column(db.Enum('Tenis', 'Pádel', 'Accesorios'), default='Accesorios')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy='dynamic')
    
    def __repr__(self):
        return f'<Producto {self.id_producto} - {self.nombre}>'

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relaciones
    detalles = db.relationship('DetalleVenta', backref='venta', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Venta {self.id_venta} - {self.fecha}>'

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<DetalleVenta {self.id_detalle}>'

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
