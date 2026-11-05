
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_workout_name"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty")
        if len(value.strip()) > 100:
            raise ValueError("Workout name cannot exceed 100 characters")
        return value.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise"
    )

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_exercise_name"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        if len(value.strip()) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters")
        return value.strip()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
        CheckConstraint("sets IS NULL OR sets > 0", name="check_sets"),
        CheckConstraint("reps IS NULL OR reps > 0", name="check_reps"),
        CheckConstraint("duration IS NULL OR duration > 0", name="check_duration"),
        CheckConstraint(
            "sets IS NOT NULL OR reps IS NOT NULL OR duration IS NOT NULL",
            name="check_exercise_details"
        ),
    )

    @validates("sets", "reps", "duration")
    def validate_values(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than zero")
        return value
