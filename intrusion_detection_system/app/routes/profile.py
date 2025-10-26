from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from app import db               # Import inside the route function
    from app.models.user import User

    user = current_user

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        existing_user = User.query.filter(
            ((User.username == username) | (User.email == email)) & (User.id != user.id)
        ).first()
        if existing_user:
            flash('Username or email already taken by another user.')
            return redirect(url_for('profile.profile'))

        user.username = username
        user.email = email
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile.profile'))

    return render_template('profile.html', user=user)


@profile_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    from app import db

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(old_password):
            flash('Old password is incorrect.')
            return redirect(url_for('profile.change_password'))

        if new_password != confirm_password:
            flash('New password and confirmation do not match.')
            return redirect(url_for('profile.change_password'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully.')
        return redirect(url_for('profile.profile'))

    return render_template('change_password.html')