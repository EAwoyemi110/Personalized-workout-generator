"""
Personalized Workout Generator - Flask Backend
"""
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from models import db, User, Workout, ProgressLog
from workout_engine import WorkoutEngine

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = 'dev-secret-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ROOT = Path(__file__).parent

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return send_from_directory(ROOT, 'index.html')


@app.route('/api/generate-workout', methods=['POST'])
def generate_workout():
    data = request.get_json() or {}
    engine = WorkoutEngine()
    workout = engine.generate(data)
    return jsonify(workout)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({'user_id': user.id, 'username': user.username})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'user_id': user.id, 'username': user.username})


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/api/me')
def me():
    if current_user.is_authenticated:
        return jsonify({'user_id': current_user.id, 'username': current_user.username})
    return jsonify({'user_id': None})


@app.route('/api/workouts', methods=['POST'])
@login_required
def save_workout():
    data = request.get_json() or {}
    workout = Workout(
        user_id=current_user.id,
        workout_type=data.get('workout_type', ''),
        exercises_json=json.dumps(data.get('exercises', [])),
        completed=data.get('completed', False)
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify({'id': workout.id})


@app.route('/api/workouts')
@login_required
def get_workouts():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.created_at.desc()).limit(50).all()
    return jsonify([{
        'id': w.id,
        'workout_type': w.workout_type,
        'exercises': json.loads(w.exercises_json or '[]'),
        'completed': w.completed,
        'created_at': w.created_at.isoformat()
    } for w in workouts])


@app.route('/api/progress', methods=['POST'])
@login_required
def log_progress():
    data = request.get_json() or {}
    log = ProgressLog(
        user_id=current_user.id,
        exercise_name=data.get('exercise_name', ''),
        reps=data.get('reps'),
        sets=data.get('sets'),
        notes=data.get('notes', '')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'id': log.id})


@app.route('/api/progress')
@login_required
def get_progress():
    logs = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.logged_at.desc()).limit(100).all()
    return jsonify([{
        'id': l.id,
        'exercise_name': l.exercise_name,
        'reps': l.reps,
        'sets': l.sets,
        'logged_at': l.logged_at.isoformat()
    } for l in logs])


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
