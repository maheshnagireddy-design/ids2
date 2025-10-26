from app import db
from datetime import datetime

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prediction = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    protocol = db.Column(db.String(10))
    src_bytes = db.Column(db.Integer)
    dst_bytes = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('detections', lazy=True))

    def __repr__(self):
        return f'<Detection {self.prediction} - {self.confidence}>'
