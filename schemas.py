
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True, load_only=True)
    exercise_id = fields.Int(required=True, load_only=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(
        "ExerciseSchema",
        dump_only=True,
        only=("id", "name", "description")
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        if not any(data.get(key) is not None for key in ("sets", "reps", "duration")):
            raise ValidationError(
                "Provide at least one of sets, reps or duration."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate.Regexp(r".*\S.*", error="Workout name cannot be blank.")
        ]
    )
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate.Regexp(r".*\S.*", error="Exercise name cannot be blank.")
        ]
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=255)
    )
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
        exclude=("exercise",)
    )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
