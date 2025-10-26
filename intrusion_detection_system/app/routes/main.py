from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User
from app.models.detection import Detection
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's detection history
    user_detections = Detection.query.filter_by(user_id=current_user.id).order_by(Detection.timestamp.desc()).limit(10).all()

    # Get statistics
    total_detections = Detection.query.filter_by(user_id=current_user.id).count()
    normal_count = Detection.query.filter_by(user_id=current_user.id, prediction='normal').count()
    attack_count = total_detections - normal_count

    stats = {
        'total_detections': total_detections,
        'normal_count': normal_count,
        'attack_count': attack_count
    }

    return render_template('main/dashboard.html', detections=user_detections, stats=stats)