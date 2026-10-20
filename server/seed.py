
from datetime import date

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=True
    )

    db.session.add_all([pushups, squats, running])
    db.session.commit()

    workout1 = Workout(
        date=date.today(),
        duration_minutes=30,
        notes="Upper body workout"
    )

    workout2 = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Legs and cardio"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    db.session.add_all([
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=pushups.id,
            reps=10,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=squats.id,
            reps=15,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=running.id,
            duration_seconds=600
        )
    ])

    db.session.commit()

    print("Seed data added successfully!")
