from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models import Usuario
from app.forms import LoginForm, RegistrationForm, ProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Correo o contraseña inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Actualizar último acceso
        user.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(
            nombre_usuario=form.nombre_usuario.data,
            email=form.email.data,
            es_admin=form.es_admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Usuario registrado exitosamente!', 'success')
        return redirect(url_for('auth.manage_users'))
    
    return render_template('auth/register.html', title='Registrar Usuario', form=form)

@auth_bp.route('/users')
@login_required
def manage_users():
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))
    
    users = Usuario.query.order_by(Usuario.nombre_usuario).all()
    return render_template('auth/users.html', title='Gestionar Usuarios', users=users)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(current_user.nombre_usuario, current_user.email)
    if form.validate_on_submit():
        current_user.nombre_usuario = form.nombre_usuario.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Tu perfil ha sido actualizado.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.nombre_usuario.data = current_user.nombre_usuario
        form.email.data = current_user.email
    
    return render_template('auth/profile.html', title='Mi Perfil', form=form)

@auth_bp.route('/edit-user/<int:id>', methods=['POST'])
@login_required
def edit_user(id):
    if not current_user.es_admin:
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = Usuario.query.get_or_404(id)
    
    # No permitir editar el propio usuario desde aquí
    if user.id == current_user.id:
        flash('No puedes editar tu propio usuario desde aquí. Usa "Mi Perfil".', 'warning')
        return redirect(url_for('auth.manage_users'))
    
    user.nombre_usuario = request.form.get('nombre_usuario')
    user.email = request.form.get('email')
    user.es_admin = 'es_admin' in request.form
    user.activo = 'activo' in request.form
    
    db.session.commit()
    flash(f'Usuario {user.nombre_usuario} actualizado correctamente.', 'success')
    return redirect(url_for('auth.manage_users'))

@auth_bp.route('/delete-user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.es_admin:
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = Usuario.query.get_or_404(id)
    
    # No permitir eliminar el propio usuario
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario.', 'danger')
        return redirect(url_for('auth.manage_users'))
    
    # Verificar que no sea el último administrador
    if user.es_admin:
        admin_count = Usuario.query.filter_by(es_admin=True, activo=True).count()
        if admin_count <= 1:
            flash('No puedes eliminar el último administrador del sistema.', 'danger')
            return redirect(url_for('auth.manage_users'))
    
    nombre = user.nombre_usuario
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario {nombre} eliminado correctamente.', 'success')
    return redirect(url_for('auth.manage_users'))

@auth_bp.route('/toggle-status/<int:id>', methods=['POST'])
@login_required
def toggle_status(id):
    if not current_user.es_admin:
        return jsonify({'success': False, 'message': 'No tienes permiso para realizar esta acción.'}), 403
    
    user = Usuario.query.get_or_404(id)
    
    # No permitir cambiar el estado del propio usuario
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'No puedes cambiar tu propio estado.'}), 400
    
    data = request.get_json()
    nuevo_estado = data.get('activo', False)
    
    # Si se está desactivando un administrador, verificar que no sea el último
    if user.es_admin and not nuevo_estado:
        admin_count = Usuario.query.filter_by(es_admin=True, activo=True).count()
        if admin_count <= 1:
            return jsonify({'success': False, 'message': 'No puedes desactivar el último administrador activo.'}), 400
    
    user.activo = nuevo_estado
    db.session.commit()
    
    estado_texto = 'activado' if nuevo_estado else 'desactivado'
    return jsonify({'success': True, 'message': f'Usuario {estado_texto} correctamente.'})
