import unittest

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


class WorkoutAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        cls.app_context = app.app_context()
        cls.app_context.push()

        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def create_workout(self, duration=30):
        workout = Workout(duration_minutes=duration, notes="Test workout")
        db.session.add(workout)
        db.session.commit()
        return workout

    def create_exercise(self, name="Push-ups"):
        exercise = Exercise(
            name=name,
            category="Strength",
            equipment_needed=False
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise

    # Home endpoint

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Workout API is running"
        )

    # Workout endpoints

    def test_get_workouts(self):
        self.create_workout()
        response = self.client.get("/workouts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_single_workout(self):
        workout = self.create_workout()
        response = self.client.get(f"/workouts/{workout.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["duration_minutes"],
            30
        )

    def test_get_missing_workout(self):
        response = self.client.get("/workouts/999")
        self.assertEqual(response.status_code, 404)

    def test_create_workout(self):
        response = self.client.post(
            "/workouts",
            json={"duration_minutes": 45, "notes": "Leg day"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json()["duration_minutes"],
            45
        )

    def test_reject_invalid_workout(self):
        response = self.client.post(
            "/workouts",
            json={"duration_minutes": 0}
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_workout(self):
        workout = self.create_workout()
        response = self.client.delete(f"/workouts/{workout.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Workout, workout.id))

    # Exercise endpoints

    def test_get_exercises(self):
        self.create_exercise()
        response = self.client.get("/exercises")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_single_exercise(self):
        exercise = self.create_exercise()
        response = self.client.get(f"/exercises/{exercise.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Push-ups")

    def test_get_missing_exercise(self):
        response = self.client.get("/exercises/999")
        self.assertEqual(response.status_code, 404)

    def test_create_exercise(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Squats",
                "category": "Strength",
                "equipment_needed": False
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Squats")

    def test_reject_exercise_without_name(self):
        response = self.client.post(
            "/exercises",
            json={
                "category": "Strength",
                "equipment_needed": False
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_exercise(self):
        exercise = self.create_exercise()
        response = self.client.delete(f"/exercises/{exercise.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Exercise, exercise.id))

    # WorkoutExercise endpoint

    def test_add_exercise_to_workout(self):
        workout = self.create_workout()
        exercise = self.create_exercise()

        response = self.client.post(
            f"/workouts/{workout.id}/exercises/"
            f"{exercise.id}/workout_exercises",
            json={"reps": 10, "sets": 3}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["reps"], 10)
        self.assertEqual(response.get_json()["sets"], 3)

    def test_reject_duplicate_exercise(self):
        workout = self.create_workout()
        exercise = self.create_exercise()

        self.client.post(
            f"/workouts/{workout.id}/exercises/"
            f"{exercise.id}/workout_exercises",
            json={"reps": 10, "sets": 3}
        )

        response = self.client.post(
            f"/workouts/{workout.id}/exercises/"
            f"{exercise.id}/workout_exercises",
            json={"reps": 8, "sets": 2}
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_missing_exercise_details(self):
        workout = self.create_workout()
        exercise = self.create_exercise()

        response = self.client.post(
            f"/workouts/{workout.id}/exercises/"
            f"{exercise.id}/workout_exercises",
            json={}
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_missing_workout(self):
        exercise = self.create_exercise()

        response = self.client.post(
            f"/workouts/999/exercises/"
            f"{exercise.id}/workout_exercises",
            json={"reps": 10}
        )

        self.assertEqual(response.status_code, 404)

    def test_reject_missing_exercise(self):
        workout = self.create_workout()

        response = self.client.post(
            f"/workouts/{workout.id}/exercises/"
            f"999/workout_exercises",
            json={"reps": 10}
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
