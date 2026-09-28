# My Courses API

A backend API for a student learning platform built with Django and Django REST Framework. The API allows authenticated students to view their enrolled courses, access course learning materials, view classroom and faculty information, track material completion, and view assignment status.

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Gunicorn
* Render

## Features

* JWT-based student authentication
* Student-specific course listing
* Course details with:

  * Classroom information
  * Faculty
  * Live sessions
  * Modules
  * Material folders
  * Study materials
  * Assignments
  * Learning progress
* Material completion tracking
* Derived assignment status
* Student-level access control to prevent unauthorized course access
* PostgreSQL database
* Seed data for testing
* Optimized course detail queries to avoid N+1 query problems

## API Endpoints

### Authentication

**POST**

```text
/api/auth/login/
```

Returns access and refresh JWT tokens.

### Course List

**GET**

```text
/api/courses/
```

Returns courses in which the authenticated student is enrolled.

### Course Details

**GET**

```text
/api/courses/<id>/
```

Returns detailed information for an enrolled course.

### Material Completion

**PATCH**

```text
/api/materials/<id>/completion/
```

Updates the completion status of a study material.

Example request:

```json
{
    "completed": true
}
```

## Authentication

The API uses JWT authentication.

After logging in, include the access token in requests:

```text
Authorization: Bearer <access_token>
```

## Test Credentials

A seeded student account is available for assessment testing:

```text
Username: rani
Password: Rani@12345
```

## Seed Data

To create the sample data locally:

```bash
python manage.py seed_data
```

The seed command creates students, courses, classrooms, faculty, modules, study materials, live sessions, assignments, submissions, and material completion records.

The command uses `get_or_create` so it can safely be run more than once.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Jyothir-mayi/my-courses-api.git
cd my-courses-api
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with the required Django secret key and PostgreSQL database settings.

Example:

```text
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=my_courses
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create sample data

```bash
python manage.py seed_data
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Live Deployment

The application is deployed on Render:

```text
https://my-courses-api-xpjq.onrender.com
```

## Project Structure

```text
MyCourses/
├── manage.py
├── MyCourses/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── courses/
    ├── migrations/
    ├── management/
    │   └── commands/
    │       └── seed_data.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Notes

Course and material data are restricted to the authenticated student's enrollments. Assignment status is derived from publication and submission timestamps rather than stored as a separate status field.

The deployed application uses PostgreSQL and is served with Gunicorn on Render.
