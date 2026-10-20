
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=False)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.Str(allow_none=True, load_default=None)
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)


class AddWorkoutExerciseSchema(Schema):
    reps = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def check_exercise_details(self, data, **kwargs):
        has_reps = data.get("reps") is not None
        has_duration = data.get("duration_seconds") is not None

        if not has_reps and not has_duration:
            raise ValidationError(
                "Provide reps for a repetition-based exercise or duration_seconds for a timed exercise."
            )
