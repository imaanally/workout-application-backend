# Workout Application Backend

## Description

This is a Flask REST API for managing workouts and exercises. It uses Flask-SQLAlchemy for the database, Flask-Migrate for migrations, and Marshmallow for validation and serialization.

## Technologies Used

- Python 3.8.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Project Structure

```text
workout-application-backend/
├── migrations/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```

## Setup

Install the dependencies:

```bash
pipenv install
```

Initialize the database migrations if they have not already been initialized:

```bash
pipenv run flask --app server.app db init
```

Create a migration:

```bash
pipenv run flask --app server.app db migrate -m "create workout tables"
```

Apply the migration:

```bash
pipenv run flask --app server.app db upgrade
```

Run the seed script:

```bash
pipenv run python -m server.seed
```

Start the API:

```bash
pipenv run flask --app server.app run
```

The API runs at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint                                                           | Description                      |
| ------ | ------------------------------------------------------------------ | -------------------------------- |
| GET    | `/workouts`                                                        | List all workouts                |
| GET    | `/workouts/<id>`                                                   | Get a workout and its exercises  |
| POST   | `/workouts`                                                        | Create a workout                 |
| DELETE | `/workouts/<id>`                                                   | Delete a workout                 |
| GET    | `/exercises`                                                       | List all exercises               |
| GET    | `/exercises/<id>`                                                  | Get an exercise and its workouts |
| POST   | `/exercises`                                                       | Create an exercise               |
| DELETE | `/exercises/<id>`                                                  | Delete an exercise               |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout     |

## Data Models

- **Exercise:** stores the exercise name, category, and whether equipment is needed.
- **Workout:** stores the date, duration, and notes.
- **WorkoutExercise:** connects workouts and exercises and stores reps, sets, and duration.

## Validation

Marshmallow schemas validate incoming request data. Model validations and database constraints help prevent invalid values and duplicate exercise entries in the same workout.

## Seed Data

The seed script clears existing records and creates sample exercises, workouts, and workout-exercise entries. It can be run again to reset the sample data.
