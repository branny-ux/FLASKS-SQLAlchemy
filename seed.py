
from app import app
from models import db, Workout, Exercise, WorkoutExercise


with app.app_context():
    db.drop_all()
    db.create_all()

    workout1 = Workout(name="Morning Workout")
    workout2 = Workout(name="Leg Day")
    workout3 = Workout(name="Full Body Workout")

    exercise1 = Exercise(
        name="Push-ups",
        description="An upper body strength exercise"
    )

    exercise2 = Exercise(
        name="Squats",
        description="A lower body strength exercise"
    )

    exercise3 = Exercise(
        name="Plank",
        description="An exercise for strengthening the core"
    )

    exercise4 = Exercise(
        name="Running",
        description="A cardiovascular exercise"
    )

    db.session.add_all([
        workout1, workout2, workout3,
        exercise1, exercise2, exercise3, exercise4
    ])

    db.session.commit()

    db.session.add_all([
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=exercise1.id,
            sets=3,
            reps=15
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=exercise2.id,
            sets=4,
            reps=12
        ),
        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=exercise3.id,
            duration=60
        ),
        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=exercise4.id,
            duration=20
        )
    ])

    db.session.commit()

    print("Workout database seeded successfully!")
