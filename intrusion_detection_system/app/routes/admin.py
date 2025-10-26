from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.detection import Detection
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_users():
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_admins():
            flash('Access denied. SuperAdmin privileges required.')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    if current_user.role == 'SuperAdmin':
        total_users = User.query.count()
    else:
        total_users = User.query.filter_by(role='User').count()

    total_detections = Detection.query.count()
    recent_detections = Detection.query.order_by(Detection.timestamp.desc()).limit(10).all()

    stats = {
        'total_users': total_users,
        'total_detections': total_detections,
        'normal_count': Detection.query.filter_by(prediction='normal').count(),
        'attack_count': Detection.query.filter(Detection.prediction != 'normal').count()
    }

    return render_template('admin/dashboard.html', stats=stats, recent_detections=recent_detections)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    if current_user.role == 'SuperAdmin':
        all_users = User.query.all()
    else:
        all_users = User.query.filter_by(role='User').all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/create_user', methods=['POST'])
@login_required
@admin_required
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    role = request.form.get('role')

    if password != confirm_password:
        flash('Password and confirmation do not match.')
        return redirect(url_for('admin.users'))

    if role == 'SuperAdmin':
        if User.query.filter_by(role='SuperAdmin').count() >= 1:
            flash('Only one SuperAdmin is allowed. Cannot create another.')
            return redirect(url_for('admin.users'))
        if not current_user.role == 'SuperAdmin':
            flash('Only SuperAdmin can create SuperAdmin users.')
            return redirect(url_for('admin.users'))

    if role == 'Admin' and not current_user.can_manage_admins():
        flash('Only SuperAdmin can create Admin users')
        return redirect(url_for('admin.users'))

    if User.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('admin.users'))

    if User.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('admin.users'))

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash(f'User {username} created successfully')
    return redirect(url_for('admin.users'))

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.role == 'SuperAdmin' and not current_user.can_manage_admins():
        flash('You cannot edit a SuperAdmin user.')
        return redirect(url_for('admin.users'))

    if user.role == 'Admin' and not current_user.can_manage_admins():
        flash('Only SuperAdmin can edit Admin users.')
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if role == 'SuperAdmin' and user.role != 'SuperAdmin':
            flash('Cannot promote a user to SuperAdmin.')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        if password:
            if password != confirm_password:
                flash('Password and confirmation do not match.')
                return redirect(url_for('admin.edit_user', user_id=user_id))
            user.set_password(password)
        
        existing_user = User.query.filter(User.id != user_id).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('Username or email already taken by another user.')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        user.username = username
        user.email = email

        if current_user.can_manage_admins():
            user.role = role

        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Cannot delete your own account.')
        return redirect(url_for('admin.users'))

    if user.role == 'SuperAdmin' and not current_user.can_manage_admins():
        flash('You cannot delete a SuperAdmin user.')
        return redirect(url_for('admin.users'))

    if user.role == 'Admin' and not current_user.can_manage_admins():
        flash('Only SuperAdmin can delete Admin users.')
        return redirect(url_for('admin.users'))

    detections = Detection.query.filter_by(user_id=user.id).all()
    for detection in detections:
        db.session.delete(detection)

    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.username} and their detection records deleted successfully.')
    return redirect(url_for('admin.users'))