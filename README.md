# Workout API

## Description

Workout API is a RESTful API built using Python and Flask. It allows users to manage workouts, exercises, and the relationships between workouts and exercises.

The project uses Flask-SQLAlchemy for database management and Marshmallow for data serialization and validation.

## Features

- Create new workouts.
- Retrieve all workouts.
- Retrieve a single workout by ID.
- Update workouts using PATCH.
- Delete workouts.
- Create new exercises.
- Retrieve all exercises.
- Retrieve a single exercise by ID.
- Delete exercises.
- Assign exercises to workouts.
- Validate incoming data using Marshmallow.
- Handle missing records and invalid requests.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv
- Pytest

## Project Structure

```text
FLASKS-SQLAlchemy/
│
├── app.py
├── config.py
├── models.py
├── schemas.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── migrations/
└── tests/
    └── test_api.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FLASKS-SQLAlchemy
```

### 2. Install dependencies

```bash
pip install pipenv
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Run database migrations

If migrations have already been created:

```bash
flask --app app db upgrade
```

### 5. Start the Flask application

```bash
flask --app app run
```

The API will be available at:

`http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workout_exercises` | Assign an exercise to a workout |

## Testing

Run the test suite using:

```bash
pipenv run pytest -v
```

## Example Request

Update a workout:

```bash
curl -X PATCH http://127.0.0.1:5000/workouts/1 \
-H "Content-Type: application/json" \
-d '{"name": "Evening Workout"}'
```

## Learning Objectives

This project demonstrates:

- Building REST APIs with Flask.
- Database relationships using SQLAlchemy.
- Object Relational Mapping (ORM).
- Data validation and serialization with Marshmallow.
- Database migrations.
- HTTP methods and status codes.
- API testing using Pytest.

## Author

Branis Beru