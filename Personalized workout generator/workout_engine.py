"""
Workout generation engine - uses quiz answers and equipment data.
"""
import random
from typing import Dict, List, Any

# Planet Fitness St. Paul equipment (typical PF inventory)
PLANET_FITNESS_EQUIPMENT = {
    'cardio': [
        'treadmill', 'elliptical', 'rowing machine', 'upright bike',
        'recumbent bike', 'stair climber', 'ARC trainer'
    ],
    'strength_machines': [
        'chest press', 'shoulder press', 'lat pulldown', 'leg press',
        'hack squat', 'cable tower', 'Smith machine', 'bicep curl',
        'tricep extension', 'preacher curl'
    ],
    'free_weights': [
        'dumbbells (5-75 lbs)', 'fixed barbells'
    ]
}

# UMD Recreation Center - typical university gym equipment
UMD_EQUIPMENT = {
    'cardio': [
        'treadmill', 'elliptical', 'rowing machine', 'bike',
        'stair climber', 'assault bike'
    ],
    'strength_machines': [
        'chest press', 'shoulder press', 'lat pulldown', 'leg press',
        'cable machine', 'Smith machine', 'leg curl', 'leg extension'
    ],
    'free_weights': [
        'dumbbells', 'barbells', 'squat rack', 'bench press'
    ]
}

# Exercise database with video placeholders (replace with your own links)
EXERCISES = {
    'planet_fitness': {
        'strength_training': [
            {'name': 'Chest Press Machine', 'sets': '3x10', 'video_embed_id': 'rT7DgCr-3pg'},
            {'name': 'Lat Pulldown', 'sets': '3x10', 'video_embed_id': 'CAwf7n6Luuc'},
            {'name': 'Leg Press', 'sets': '3x12', 'video_embed_id': '2U3CbRlHpY'},
            {'name': 'Shoulder Press Machine', 'sets': '3x10', 'video_embed_id': 'qEwKCR5JCog'},
            {'name': 'Dumbbell Bicep Curls', 'sets': '3x12', 'video_embed_id': 'ykJmrZ5v0Oo'},
            {'name': 'Tricep Extension Machine', 'sets': '3x12', 'video_embed_id': '6Z15_WdXmVw'},
        ],
        'cardio': [
            {'name': 'Treadmill – Incline Walk', 'sets': '20 min'},
            {'name': 'Elliptical', 'sets': '15 min'},
            {'name': 'Rowing Machine', 'sets': '10 min', 'video_embed_id': '0cBjM-9D0cM'},
        ],
        'calisthenics': [
            {'name': 'Push-ups', 'sets': '3x10', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Bodyweight Squats', 'sets': '3x15', 'video_embed_id': 'acLH3-2EPLc'},
            {'name': 'Plank', 'sets': '3x30 sec', 'video_embed_id': 'pSHjTRCQxIw'},
            {'name': 'Mountain Climbers', 'sets': '3x20', 'video_embed_id': 'nmwgirgXLYM'},
        ],
        'mixed': [
            {'name': 'Warm-up: 5 min light cardio', 'sets': '5 min'},
            {'name': 'Chest Press Machine', 'sets': '3x10', 'video_embed_id': 'rT7DgCr-3pg'},
            {'name': 'Bodyweight Squats', 'sets': '3x15', 'video_embed_id': 'acLH3-2EPLc'},
            {'name': 'Lat Pulldown', 'sets': '3x10', 'video_embed_id': 'CAwf7n6Luuc'},
            {'name': 'Plank', 'sets': '3x30 sec', 'video_embed_id': 'pSHjTRCQxIw'},
            {'name': 'Cool-down: 5 min stretch', 'sets': '5 min'},
        ],
    },
    'umd': {
        'strength_training': [
            {'name': 'Barbell Bench Press', 'sets': '3x8', 'video_embed_id': 'rT7DgCr-3pg'},
            {'name': 'Barbell Back Squat', 'sets': '3x8', 'video_embed_id': 'ultWZbUMPL8'},
            {'name': 'Lat Pulldown', 'sets': '3x10', 'video_embed_id': 'CAwf7n6Luuc'},
            {'name': 'Overhead Press', 'sets': '3x8', 'video_embed_id': 'qEwKCR5JCog'},
            {'name': 'Romanian Deadlift', 'sets': '3x10', 'video_embed_id': 'JCXUYuzwNrM'},
        ],
        'cardio': [
            {'name': 'Treadmill HIIT', 'sets': '20 min'},
            {'name': 'Rowing Machine', 'sets': '15 min', 'video_embed_id': '0cBjM-9D0cM'},
        ],
        'calisthenics': [
            {'name': 'Pull-ups', 'sets': '3x8', 'video_embed_id': 'eGo4IYlbE5g'},
            {'name': 'Push-ups', 'sets': '3x12', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Lunges', 'sets': '3x10 each', 'video_embed_id': 'QOVaHwm-Q6U'},
            {'name': 'Plank', 'sets': '3x45 sec', 'video_embed_id': 'pSHjTRCQxIw'},
        ],
        'mixed': [
            {'name': 'Warm-up: 5 min cardio', 'sets': '5 min'},
            {'name': 'Barbell Squat', 'sets': '3x8', 'video_embed_id': 'ultWZbUMPL8'},
            {'name': 'Push-ups', 'sets': '3x12', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Lat Pulldown', 'sets': '3x10', 'video_embed_id': 'CAwf7n6Luuc'},
            {'name': 'Plank', 'sets': '3x30 sec', 'video_embed_id': 'pSHjTRCQxIw'},
        ],
    },
    'home': {
        'strength_training': [
            {'name': 'Push-up variations', 'sets': '3x10', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Pike push-ups', 'sets': '3x8', 'video_embed_id': 'lTodERndpKw'},
            {'name': 'Bodyweight rows (table)', 'sets': '3x10', 'video_embed_id': 'p44LXO-sB8E'},
        ],
        'cardio': [
            {'name': 'Jumping jacks', 'sets': '3x1 min'},
            {'name': 'High knees', 'sets': '3x30 sec'},
            {'name': 'Burpees', 'sets': '3x8', 'video_embed_id': 'TU8QYVW0gDU'},
        ],
        'calisthenics': [
            {'name': 'Push-ups', 'sets': '3x12', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Squats', 'sets': '3x15', 'video_embed_id': 'acLH3-2EPLc'},
            {'name': 'Lunges', 'sets': '3x10 each', 'video_embed_id': 'QOVaHwm-Q6U'},
            {'name': 'Plank', 'sets': '3x45 sec', 'video_embed_id': 'pSHjTRCQxIw'},
            {'name': 'Glute bridge', 'sets': '3x15', 'video_embed_id': 'wPM8icPu6H4'},
        ],
        'mixed': [
            {'name': 'Warm-up: Dynamic stretch', 'sets': '5 min'},
            {'name': 'Push-ups', 'sets': '3x10', 'video_embed_id': 'IODxDxX7oi4'},
            {'name': 'Squats', 'sets': '3x15', 'video_embed_id': 'acLH3-2EPLc'},
            {'name': 'Plank', 'sets': '3x30 sec', 'video_embed_id': 'pSHjTRCQxIw'},
            {'name': 'Cool-down stretch', 'sets': '5 min'},
        ],
    },
}


class WorkoutEngine:
    """Generates personalized workouts from form or quiz answers."""

    def generate(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        equipment = answers.get('equipment', [])
        exercise_types = answers.get('exercise_type', [])
        reps = answers.get('reps', 10)

        # Support both new form format (arrays) and old quiz format (single values)
        if isinstance(equipment, str):
            equipment_key = 'planet_fitness' if equipment == 'planet_fitness' else 'umd' if equipment == 'umd' else 'home'
        else:
            # Form: equipment = ['treadmill','weights','bike','yoga_ball','pull_up_bar']
            if not equipment or 'weights' in equipment or 'treadmill' in equipment:
                equipment_key = 'planet_fitness'
            elif 'pull_up_bar' in equipment and not any(e in equipment for e in ['treadmill', 'weights']):
                equipment_key = 'home'
            else:
                equipment_key = 'planet_fitness'

        if isinstance(exercise_types, str):
            workout_type = exercise_types
        else:
            # Form: exercise_type = ['cardio','strength','flexibility','balance','stamina']
            if 'strength' in exercise_types:
                workout_type = 'strength_training'
            elif 'cardio' in exercise_types:
                workout_type = 'cardio'
            elif 'flexibility' in exercise_types or 'balance' in exercise_types:
                workout_type = 'calisthenics'
            else:
                workout_type = 'mixed'

        exercises = EXERCISES.get(equipment_key, EXERCISES['planet_fitness']).get(
            workout_type, EXERCISES['planet_fitness']['mixed']
        ).copy()

        # Apply reps to exercises that use numeric sets (e.g. 3x10 -> 3x{reps})
        def apply_reps(ex: dict, r: int) -> dict:
            s = ex.get('sets', '3x10')
            if 'x' in s and 'min' not in s.lower() and 'sec' not in s.lower():
                parts = s.split('x')
                if len(parts) >= 2 and parts[1].strip().isdigit():
                    ex = dict(ex)
                    ex['sets'] = f'{parts[0].strip()}x{r}'
            return ex

        exercises = [apply_reps(dict(e), reps) for e in exercises]

        return {
            'workout_type': workout_type,
            'equipment': equipment_key,
            'exercises': exercises,
        }
