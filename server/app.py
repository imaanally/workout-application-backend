
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ExerciseSchema,
    WorkoutSchema,
    AddWorkoutExerciseSchema
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workouts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
add_exercise_schema = AddWorkoutExerciseSchema()


@app.route("/")
def home():
    return jsonify({"message": "Workout API is running"})


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    result = workout_schema.dump(workout)
    result["workout_exercises"] = [
        {
            "exercise": exercise_schema.dump(item.exercise),
            "reps": item.reps,
            "sets": item.sets,
            "duration_seconds": item.duration_seconds
        }
        for item in workout.workout_exercises
    ]
    return jsonify(result), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        workout_data = workout_schema.load(data)
        workout = Workout(
            date=workout_data.get("date"),
            duration_minutes=workout_data["duration_minutes"],
            notes=workout_data.get("notes")
        )
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400
    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    result = exercise_schema.dump(exercise)
    result["workouts"] = [
        {
            "workout_id": item.workout_id,
            "date": item.workout.date.isoformat(),
            "reps": item.reps,
            "sets": item.sets,
            "duration_seconds": item.duration_seconds
        }
        for item in exercise.workout_exercises
    ]
    return jsonify(result), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        exercise_data = exercise_schema.load(data)
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400
    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing:
        return jsonify({
            "error": "This exercise is already in the workout"
        }), 400

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body is required"}), 400

    try:
        details = add_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=details.get("reps"),
            sets=details.get("sets"),
            duration_seconds=details.get("duration_seconds")
        )
        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise added to workout",
            "id": workout_exercise.id,
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds
        }), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "This exercise is already in the workout"
        }), 400
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
