from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DecimalField, IntegerField, FileField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from wtforms.widgets import NumberInput
from app.models import Usuario

# ================================
# FORMULARIOS DE AUTENTICACIÓN
# ================================

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    password2 = PasswordField(
        'Repetir Contraseña',
        validators=[
            DataRequired(),
            EqualTo('password', message='Las contraseñas no coinciden')
        ]
    )
    es_admin = BooleanField('Es Administrador')
    submit = SubmitField('Registrar')

    def validate_username(self, nombre_usuario):
        user = Usuario.query.filter_by(nombre_usuario=nombre_usuario.data).first()
        if user is not None:
            raise ValidationError('Por favor usa un nombre de usuario diferente.')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor usa una dirección de correo diferente.')

class ProfileForm(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Nueva Contraseña (dejar en blanco para no cambiar)')
    password2 = PasswordField(
        'Repetir Contraseña',
        validators=[EqualTo('password', message='Las contraseñas no coinciden')]
    )
    submit = SubmitField('Actualizar Perfil')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, nombre_usuario):
        if nombre_usuario.data != self.original_username:
            user = Usuario.query.filter_by(nombre_usuario=nombre_usuario.data).first()
            if user is not None:
                raise ValidationError('Por favor usa un nombre de usuario diferente.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = Usuario.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Por favor usa una dirección de correo diferente.')

# ================================
# FORMULARIOS DE PRODUCTOS
# ================================

class ProductoForm(FlaskForm):
    """Formulario para agregar/editar productos"""
    codigo = StringField('Código', validators=[
        DataRequired(message='El código es requerido'),
        Length(max=20, message='El código no puede tener más de 20 caracteres')
    ])
    
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='El nombre no puede tener más de 100 caracteres')
    ])
    
    descripcion = TextAreaField('Descripción', validators=[
        Optional(),
        Length(max=500, message='La descripción no puede tener más de 500 caracteres')
    ])
    
    precio_compra = DecimalField('Precio de Compra', validators=[
        DataRequired(message='El precio de compra es requerido'),
        NumberRange(min=0, message='El precio no puede ser negativo')
    ], places=2)
    
    precio_venta = DecimalField('Precio de Venta', validators=[
        DataRequired(message='El precio de venta es requerido'),
        NumberRange(min=0, message='El precio no puede ser negativo')
    ], places=2)
    
    stock_inicial = IntegerField('Stock Inicial', validators=[
        DataRequired(message='El stock inicial es requerido'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ], default=0)
    
    stock_minimo = IntegerField('Stock Mínimo', validators=[
        DataRequired(message='El stock mínimo es requerido'),
        NumberRange(min=0, message='El stock mínimo no puede ser negativo')
    ], default=5)
    
    categoria = SelectField('Categoría', choices=[
        ('Tenis', 'Tenis'),
        ('Pádel', 'Pádel'),
        ('Accesorios', 'Accesorios')
    ], validators=[DataRequired()])
    
    marca = StringField('Marca', validators=[
        Optional(),
        Length(max=50, message='La marca no puede tener más de 50 caracteres')
    ])
    
    talla = StringField('Talla', validators=[
        Optional(),
        Length(max=10, message='La talla no puede tener más de 10 caracteres')
    ])
    
    color = StringField('Color', validators=[
        Optional(),
        Length(max=30, message='El color no puede tener más de 30 caracteres')
    ])
    
    imagen = FileField('Imagen del Producto')


class AjusteInventarioForm(FlaskForm):
    """Formulario para ajustar el inventario de un producto"""
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message='La cantidad es requerida')
    ])
    
    notas = TextAreaField('Notas', validators=[
        Optional(),
        Length(max=255, message='Las notas no pueden tener más de 255 caracteres')
    ])

# ================================
# FORMULARIOS DE VENTAS
# ================================

class VentaForm(FlaskForm):
    """Formulario para registrar una nueva venta"""
    cliente_id = SelectField('Cliente', coerce=str, validators=[Optional()])
    
    metodo_pago = SelectField('Método de Pago', choices=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ], validators=[DataRequired(message='Selecciona un método de pago')])
    
    notas = TextAreaField('Notas', validators=[
        Optional(),
        Length(max=500, message='Las notas no pueden tener más de 500 caracteres')
    ])
    
    # Campo oculto para almacenar los detalles de la venta en formato JSON
    detalles_venta = HiddenField('Detalles de la Venta', validators=[
        DataRequired(message='Debes agregar al menos un producto a la venta')
    ])


class ClienteForm(FlaskForm):
    """Formulario para agregar/editar clientes"""
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='El nombre no puede tener más de 100 caracteres')
    ])
    
    apellido = StringField('Apellido', validators=[
        Optional(),
        Length(max=100, message='El apellido no puede tener más de 100 caracteres')
    ])
    
    email = StringField('Correo Electrónico', validators=[
        Optional(),
        Length(max=120, message='El correo no puede tener más de 120 caracteres')
    ])
    
    telefono = StringField('Teléfono', validators=[
        Optional(),
        Length(max=20, message='El teléfono no puede tener más de 20 caracteres')
    ])
    
    direccion = StringField('Dirección', validators=[
        Optional(),
        Length(max=200, message='La dirección no puede tener más de 200 caracteres')
    ])


class FiltroVentasForm(FlaskForm):
    """Formulario para filtrar ventas"""
    fecha_inicio = DateField('Fecha Inicio', format='%Y-%m-%d', validators=[Optional()])
    fecha_fin = DateField('Fecha Fin', format='%Y-%m-%d', validators=[Optional()])
    
    estado = SelectField('Estado', choices=[
        ('', 'Todos los estados'),
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('anulada', 'Anulada')
    ], validators=[Optional()])
    
    metodo_pago = SelectField('Método de Pago', choices=[
        ('', 'Todos los métodos'),
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ], validators=[Optional()])
    
    cliente_id = SelectField('Cliente', coerce=str, validators=[Optional()])
