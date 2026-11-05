
import pytest

from app import create_app
from models import db, Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://"
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Workout API is running"


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={"name": "Morning Workout"}
    )

    assert response.status_code == 201
    assert response.json["name"] == "Morning Workout"


def test_create_workout_with_invalid_name(client):
    response = client.post(
        "/workouts",
        json={"name": ""}
    )

    assert response.status_code == 400


def test_get_workouts(client):
    client.post("/workouts", json={"name": "Leg Day"})

    response = client.get("/workouts")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Push-ups",
            "description": "Upper body exercise"
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "Push-ups"


def test_add_exercise_to_workout(client):
    workout = client.post(
        "/workouts",
        json={"name": "Full Body Workout"}
    )

    exercise = client.post(
        "/exercises",
        json={"name": "Squats"}
    )

    response = client.post(
        "/workout_exercises",
        json={
            "workout_id": workout.json["id"],
            "exercise_id": exercise.json["id"],
            "sets": 3,
            "reps": 12
        }
    )

    assert response.status_code == 201
    assert response.json["workout_exercise"]["sets"] == 3


def test_add_exercise_with_invalid_sets(client):
    workout = client.post(
        "/workouts",
        json={"name": "Leg Day"}
    )

    exercise = client.post(
        "/exercises",
        json={"name": "Squats"}
    )

    response = client.post(
        "/workout_exercises",
        json={
            "workout_id": workout.json["id"],
            "exercise_id": exercise.json["id"],
            "sets": 0,
            "reps": 12
        }
    )

    assert response.status_code == 400


def test_delete_workout(client):
    workout = client.post(
        "/workouts",
        json={"name": "Morning Workout"}
    )

    response = client.delete(
        f"/workouts/{workout.json['id']}"
    )

    assert response.status_code == 200


def test_get_missing_workout(client):
    response = client.get("/workouts/100")

    assert response.status_code == 404


def test_delete_missing_exercise(client):
    response = client.delete("/exercises/100")

    assert response.status_code == 404
