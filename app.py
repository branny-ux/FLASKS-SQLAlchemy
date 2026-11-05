

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from config import Config
from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    @app.route("/")
    def home():
        return jsonify({"message": "Workout API is running"})

    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(workouts)), 200

    @app.route("/workouts/<int:id>", methods=["GET"])
    def get_workout(id):
        workout = db.session.get(Workout, id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        return jsonify(workout_schema.dump(workout)), 200

    @app.route("/workouts", methods=["POST"])
    def create_workout():
        try:
            data = workout_schema.load(request.get_json() or {})
            workout = Workout(**data)

            db.session.add(workout)
            db.session.commit()

            return jsonify(workout_schema.dump(workout)), 201

        except ValidationError as error:
            db.session.rollback()
            return jsonify({"errors": error.messages}), 400

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Workout could not be created"}), 400

    @app.route("/workouts/<int:id>", methods=["PATCH"])
    def update_workout(id):
        workout = db.session.get(Workout, id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        try:
            data = workout_schema.load(
                request.get_json() or {},
                partial=True
            )

            for key, value in data.items():
                setattr(workout, key, value)

            db.session.commit()

            return jsonify(workout_schema.dump(workout)), 200

        except ValidationError as error:
            db.session.rollback()
            return jsonify({"errors": error.messages}), 400

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Workout could not be updated"}), 400

    @app.route("/workouts/<int:id>", methods=["DELETE"])
    def delete_workout(id):
        workout = db.session.get(Workout, id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        db.session.delete(workout)
        db.session.commit()

        return jsonify({"message": "Workout deleted successfully"}), 200

    @app.route("/exercises", methods=["GET"])
    def get_exercises():
        exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(exercises)), 200

    @app.route("/exercises/<int:id>", methods=["GET"])
    def get_exercise(id):
        exercise = db.session.get(Exercise, id)

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        return jsonify(exercise_schema.dump(exercise)), 200

    @app.route("/exercises", methods=["POST"])
    def create_exercise():
        try:
            data = exercise_schema.load(request.get_json() or {})
            exercise = Exercise(**data)

            db.session.add(exercise)
            db.session.commit()

            return jsonify(exercise_schema.dump(exercise)), 201

        except ValidationError as error:
            db.session.rollback()
            return jsonify({"errors": error.messages}), 400

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Exercise could not be created"}), 400

    @app.route("/exercises/<int:id>", methods=["DELETE"])
    def delete_exercise(id):
        exercise = db.session.get(Exercise, id)

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        if exercise.workout_exercises:
            return jsonify({
                "error": "Exercise is already assigned to a workout"
            }), 400

        db.session.delete(exercise)
        db.session.commit()

        return jsonify({"message": "Exercise deleted successfully"}), 200

    @app.route("/workout_exercises", methods=["POST"])
    def add_exercise_to_workout():
        try:
            data = workout_exercise_schema.load(request.get_json() or {})

            workout = db.session.get(Workout, data["workout_id"])
            exercise = db.session.get(Exercise, data["exercise_id"])

            if not workout:
                return jsonify({"error": "Workout not found"}), 404

            if not exercise:
                return jsonify({"error": "Exercise not found"}), 404

            workout_exercise = WorkoutExercise(**data)

            db.session.add(workout_exercise)
            db.session.commit()

            return jsonify({
                "message": "Exercise added to workout successfully",
                "workout_exercise": {
                    "id": workout_exercise.id,
                    "workout_id": workout_exercise.workout_id,
                    "exercise_id": workout_exercise.exercise_id,
                    "sets": workout_exercise.sets,
                    "reps": workout_exercise.reps,
                    "duration": workout_exercise.duration
                }
            }), 201

        except ValidationError as error:
            db.session.rollback()
            return jsonify({"errors": error.messages}), 400

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Exercise could not be added"}), 400

    return app


app = create_app()
