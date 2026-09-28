from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection

from rest_framework.test import APIClient

from .models import (
    Faculty,
    Course,
    Classroom,
    Enrollment,
    Module,
    MaterialFolder,
    StudyMaterial,
    LiveSession,
    Assignment,
    AssignmentSubmission,
    MaterialCompletion,
)


class CourseDetailQueryTest(TestCase):

    def setUp(self):
        # Create student
        self.student = User.objects.create_user(
            username="teststudent",
            password="testpassword"
        )

        # Create faculty
        faculty = Faculty.objects.create(
            name="Test Faculty",
            email="faculty@example.com"
        )

        # Create course
        self.course = Course.objects.create(
            name="Test Python Course",
            description="Test course description"
        )

        # Create classroom
        classroom = Classroom.objects.create(
            course=self.course,
            name="Test Batch"
        )
        classroom.faculty.add(faculty)

        # Enroll student
        Enrollment.objects.create(
            student=self.student,
            course=self.course,
            classroom=classroom
        )

        # Create live session
        LiveSession.objects.create(
            classroom=classroom,
            title="Python Introduction",
            scheduled_at="2026-10-01T10:00:00Z",
            meeting_url="https://example.com/meeting"
        )

        # Create module
        module = Module.objects.create(
            course=self.course,
            title="Python Fundamentals",
            order=1
        )

        # Create folder
        folder = MaterialFolder.objects.create(
            module=module,
            name="Python Basics"
        )

        # Create materials
        material1 = StudyMaterial.objects.create(
            folder=folder,
            title="Variables",
            material_type="PDF",
            url="https://example.com/variables"
        )

        material2 = StudyMaterial.objects.create(
            folder=folder,
            title="Functions",
            material_type="PDF",
            url="https://example.com/functions"
        )

        # Create completion record
        MaterialCompletion.objects.create(
            student=self.student,
            material=material1,
            completed=True
        )

        # Create assignment
        assignment = Assignment.objects.create(
            course=self.course,
            title="Python Assignment",
            description="Complete the Python exercises.",
            due_date="2026-10-10T10:00:00Z",
            published=True
        )

        # Create submission
        AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.student,
            submitted_at="2026-10-05T10:00:00Z"
        )

        # API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

    def test_course_detail_query_count(self):

        with CaptureQueriesContext(connection) as queries:

            response = self.client.get(
                f"/api/courses/{self.course.id}/"
            )

        self.assertEqual(response.status_code, 200)

        query_count = len(queries)

        print(f"\nCourse detail database queries: {query_count}")

        for index, query in enumerate(queries, start=1):
            print(f"\nQUERY {index}:")
            print(query["sql"])

        self.assertLessEqual(query_count, 10)