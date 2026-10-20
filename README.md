# Workout Application Backend

## Description

This project is a Flask REST API for managing workouts and exercises. Users can create, view, and delete workouts and exercises, and add exercises to workouts with details such as reps, sets, and duration.

The application uses Flask-SQLAlchemy for database management, Flask-Migrate for database migrations, and Marshmallow for serialization, deserialization, and schema validation.

## Technologies Used

- Python 3.8.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLAlchemy
- SQLite
- Pipenv

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
├── .python-version
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/imaanally/workout-application-backend.git
cd workout-application-backend
```

### 2. Install dependencies

Install the required packages using Pipenv:

```bash
pipenv install
```

### 3. Set up the database

Apply the existing database migrations:

```bash
pipenv run flask --app server.app db upgrade
```

If you are developing new models or changing the database schema, create and apply a new migration:

```bash
pipenv run flask --app server.app db migrate -m "describe your changes"
pipenv run flask --app server.app db upgrade
```

Initialize migrations with `db init` only if the migrations directory has not already been created.

### 4. Seed the database

Run the seed script to create sample exercises, workouts, and workout-exercise records:

```bash
pipenv run python -m server.seed
```

The seed script clears existing sample records before creating new ones. Running it again resets the sample data.

### 5. Run the application

Start the Flask development server:

```bash
pipenv run flask --app server.app run
```

The API will be available at:

`http://127.0.0.1:5000`

Visit the root endpoint to check that the API is running:

`http://127.0.0.1:5000/`

## API Endpoints

| Method | Endpoint                                                           | Description                                                       |
| ------ | ------------------------------------------------------------------ | ----------------------------------------------------------------- |
| GET    | `/workouts`                                                        | Retrieve all workouts                                             |
| GET    | `/workouts/<id>`                                                   | Retrieve one workout and its associated exercises                 |
| POST   | `/workouts`                                                        | Create a new workout                                              |
| DELETE | `/workouts/<id>`                                                   | Delete a workout and its associated join records                  |
| GET    | `/exercises`                                                       | Retrieve all exercises                                            |
| GET    | `/exercises/<id>`                                                  | Retrieve one exercise and its associated workouts                 |
| POST   | `/exercises`                                                       | Create a new exercise                                             |
| DELETE | `/exercises/<id>`                                                  | Delete an exercise and its associated join records                |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps, sets, or duration details |

## Data Models

### Exercise

Stores information about an exercise.

- `id`: Integer primary key
- `name`: Exercise name
- `category`: Exercise category
- `equipment_needed`: Boolean indicating whether equipment is required

### Workout

Stores information about a workout session.

- `id`: Integer primary key
- `date`: Date of the workout, defaulting to the current date
- `duration_minutes`: Workout duration in minutes
- `notes`: Optional notes about the workout

### WorkoutExercise

Connects workouts and exercises and stores details specific to an exercise within a workout.

- `id`: Integer primary key
- `workout_id`: Foreign key referencing a workout
- `exercise_id`: Foreign key referencing an exercise
- `reps`: Number of repetitions
- `sets`: Number of sets
- `duration_seconds`: Duration for timed exercises

## Relationships

- A workout has many workout-exercise records.
- An exercise has many workout-exercise records.
- Each workout-exercise record belongs to one workout and one exercise.
- Workouts and exercises are connected through the workout-exercise join table.
- Workouts can access their associated exercises, and exercises can access their associated workouts.

## Validation

The application uses multiple levels of validation to maintain data integrity.

### Schema Validations

Marshmallow schemas validate incoming request data, including:

- Required exercise fields and allowed text lengths.
- Positive workout duration, reps, sets, and timed duration.
- The requirement to provide reps or a duration when adding an exercise to a workout.

### Model Validations

Model-level validation prevents invalid values, including:

- Empty or whitespace-only exercise names and categories.
- Non-positive workout durations.
- Non-positive reps, sets, and timed durations.

### Database Constraints

Database constraints enforce rules such as:

- Positive workout duration.
- Positive reps, sets, and timed durations when provided.
- Non-empty exercise names and categories.
- No duplicate exercise entries for the same workout.

## Error Handling

The API returns JSON error messages for invalid request data and missing resources. It also handles attempts to add the same exercise to a workout more than once.

## License

This project was created as part of a Flask SQLAlchemy backend development lab.
