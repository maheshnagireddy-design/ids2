from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from app import db
from app.models.detection import Detection
import joblib
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

detection_bp = Blueprint('detection', __name__)

def load_ml_model():
    """Load the trained Random Forest model"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'models', 'intrusion_detection_model.pkl')
        if not os.path.exists(model_path):
            # Try alternate path
            model_path = 'intrusion_detection_model.pkl'

        model_data = joblib.load(model_path)
        return model_data
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@detection_bp.route('/live')
@login_required
def live_detection():
    return render_template('detection/live_detection.html')

@detection_bp.route('/results')
@login_required
def results():
    user_detections = Detection.query.filter_by(user_id=current_user.id).order_by(Detection.timestamp.desc()).all()
    return render_template('detection/results.html', detections=user_detections)

@detection_bp.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()

        # Load the model
        model_data = load_ml_model()
        if not model_data:
            return jsonify({'error': 'Model not available'}), 500

        model = model_data['model']
        encoders = model_data['label_encoders']
        feature_names = model_data['feature_names']

        # Prepare sample data
        sample_df = pd.DataFrame([data])

        # Encode categorical variables
        for feature in encoders:
            if feature in sample_df.columns:
                try:
                    sample_df[feature] = encoders[feature].transform(sample_df[feature])
                except ValueError:
                    # Handle unknown categories
                    sample_df[feature] = 0

        # Ensure all features are present
        sample_array = np.zeros(len(feature_names))
        for i, feature in enumerate(feature_names):
            if feature in sample_df.columns:
                sample_array[i] = sample_df[feature].iloc[0]

        # Make prediction
        prediction = model.predict([sample_array])[0]
        probability = model.predict_proba([sample_array])[0]
        confidence = max(probability)

        # Save detection to database
        detection = Detection(
            user_id=current_user.id,
            prediction=prediction,
            confidence=confidence,
            ip_address=data.get('src_ip', 'Unknown'),
            protocol=data.get('protocol_type', 'Unknown'),
            src_bytes=int(data.get('src_bytes', 0)),
            dst_bytes=int(data.get('dst_bytes', 0))
        )
        db.session.add(detection)
        db.session.commit()

        return jsonify({
            'prediction': prediction,
            'confidence': float(confidence),
            'probabilities': {cls: float(prob) for cls, prob in zip(model_data['attack_classes'], probability)},
            'timestamp': detection.timestamp.isoformat(),
            'is_attack': prediction != 'normal'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@detection_bp.route('/api/simulate', methods=['POST'])
@login_required
def simulate_traffic():
    """Simulate network traffic for demonstration"""
    try:
        # Generate random network traffic samples
        samples = []
        attack_types = ['normal', 'dos', 'probe', 'r2l', 'u2r']

        for _ in range(5):
            sample = {
                'duration': np.random.exponential(50),
                'protocol_type': np.random.choice(['tcp', 'udp', 'icmp']),
                'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet']),
                'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR']),
                'src_bytes': int(np.random.exponential(1000)),
                'dst_bytes': int(np.random.exponential(500)),
                'land': int(np.random.choice([0, 1], p=[0.99, 0.01])),
                'wrong_fragment': int(np.random.poisson(0.1)),
                'urgent': int(np.random.poisson(0.01)),
                'hot': int(np.random.poisson(0.5)),
                'num_failed_logins': int(np.random.poisson(0.1)),
                'logged_in': int(np.random.choice([0, 1], p=[0.3, 0.7])),
                'num_compromised': int(np.random.poisson(0.1)),
                'root_shell': int(np.random.poisson(0.05)),
                'su_attempted': int(np.random.poisson(0.01)),
                'num_root': int(np.random.poisson(0.1)),
                'num_file_creations': int(np.random.poisson(0.1)),
                'num_shells': int(np.random.poisson(0.05)),
                'num_access_files': int(np.random.poisson(0.1)),
                'num_outbound_cmds': int(np.random.poisson(0.01)),
                'is_host_login': int(np.random.choice([0, 1], p=[0.95, 0.05])),
                'is_guest_login': int(np.random.choice([0, 1], p=[0.95, 0.05])),
                'count': int(np.random.poisson(10)),
                'srv_count': int(np.random.poisson(8)),
                'serror_rate': float(np.random.uniform(0, 1)),
                'srv_serror_rate': float(np.random.uniform(0, 1)),
                'rerror_rate': float(np.random.uniform(0, 1)),
                'srv_rerror_rate': float(np.random.uniform(0, 1)),
                'same_srv_rate': float(np.random.uniform(0, 1)),
                'diff_srv_rate': float(np.random.uniform(0, 1)),
                'srv_diff_host_rate': float(np.random.uniform(0, 1)),
                'dst_host_count': int(np.random.poisson(50)),
                'dst_host_srv_count': int(np.random.poisson(30)),
                'dst_host_same_srv_rate': float(np.random.uniform(0, 1)),
                'dst_host_diff_srv_rate': float(np.random.uniform(0, 1)),
                'dst_host_same_src_port_rate': float(np.random.uniform(0, 1)),
                'dst_host_srv_diff_host_rate': float(np.random.uniform(0, 1)),
                'dst_host_serror_rate': float(np.random.uniform(0, 1)),
                'dst_host_srv_serror_rate': float(np.random.uniform(0, 1)),
                'dst_host_rerror_rate': float(np.random.uniform(0, 1)),
                'dst_host_srv_rerror_rate': float(np.random.uniform(0, 1)),
                'src_ip': f"192.168.1.{np.random.randint(1, 255)}"
            }
            samples.append(sample)

        return jsonify({'samples': samples})

    except Exception as e:
        return jsonify({'error': str(e)}), 500