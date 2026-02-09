"""Database models for user accounts and progress tracking."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User account."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workouts = db.relationship('Workout', backref='user', lazy=True)
    progress_logs = db.relationship('ProgressLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Workout(db.Model):
    """Saved workout session."""
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_type = db.Column(db.String(50))
    exercises_json = db.Column(db.Text)  # JSON string of exercises
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ProgressLog(db.Model):
    """Individual exercise progress (reps, weight, etc.)."""
    __tablename__ = 'progress_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_name = db.Column(db.String(120), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    notes = db.Column(db.String(256))
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
