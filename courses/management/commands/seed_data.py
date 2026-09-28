from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from courses.models import (
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


class Command(BaseCommand):
    help = "Seeds the database with realistic sample data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Creating seed data...")

        # --------------------------------------------------
        # 1. STUDENTS
        # --------------------------------------------------

        student1, created = User.objects.get_or_create(
            username="rani",
            defaults={
                "first_name": "Rani",
                "last_name": "Jyothirmayi",
                "email": "rani@example.com",
            }
        )

        if created:
            student1.set_password("Rani@12345")
            student1.save()

        student2, created = User.objects.get_or_create(
            username="arun",
            defaults={
                "first_name": "Arun",
                "last_name": "Kumar",
                "email": "arun@example.com",
            }
        )

        if created:
            student2.set_password("Arun@12345")
            student2.save()

        # --------------------------------------------------
        # 2. FACULTY
        # --------------------------------------------------

        faculty1, _ = Faculty.objects.get_or_create(
            email="anitha@example.com",
            defaults={
                "name": "Dr. Anitha Menon",
            }
        )

        faculty2, _ = Faculty.objects.get_or_create(
            email="rahul@example.com",
            defaults={
                "name": "Rahul Nair",
            }
        )

        # --------------------------------------------------
        # 3. COURSES
        # --------------------------------------------------

        python_course, _ = Course.objects.get_or_create(
            name="Python & Django Development",
            defaults={
                "description": (
                    "Learn Python programming, Django web development, "
                    "REST APIs and database integration."
                )
            }
        )

        database_course, _ = Course.objects.get_or_create(
            name="Database & SQL Fundamentals",
            defaults={
                "description": (
                    "Learn relational databases, SQL queries, "
                    "PostgreSQL and database design."
                )
            }
        )

        # --------------------------------------------------
        # 4. CLASSROOMS
        # --------------------------------------------------

        python_classroom, _ = Classroom.objects.get_or_create(
            course=python_course,
            name="Python Batch A"
        )

        python_classroom.faculty.set([faculty1, faculty2])

        database_classroom, _ = Classroom.objects.get_or_create(
            course=database_course,
            name="Database Batch A"
        )

        database_classroom.faculty.set([faculty2])

        # --------------------------------------------------
        # 5. ENROLLMENTS
        # --------------------------------------------------

        Enrollment.objects.get_or_create(
            student=student1,
            course=python_course,
            defaults={
                "classroom": python_classroom
            }
        )

        Enrollment.objects.get_or_create(
            student=student1,
            course=database_course,
            defaults={
                "classroom": None
            }
        )

        Enrollment.objects.get_or_create(
            student=student2,
            course=python_course,
            defaults={
                "classroom": python_classroom
            }
        )

        # --------------------------------------------------
        # 6. MODULES
        # --------------------------------------------------

        python_module1, _ = Module.objects.get_or_create(
            course=python_course,
            title="Python Fundamentals",
            defaults={"order": 1}
        )

        python_module2, _ = Module.objects.get_or_create(
            course=python_course,
            title="Django & REST APIs",
            defaults={"order": 2}
        )

        database_module1, _ = Module.objects.get_or_create(
            course=database_course,
            title="SQL Fundamentals",
            defaults={"order": 1}
        )

        # --------------------------------------------------
        # 7. MATERIAL FOLDERS
        # --------------------------------------------------

        python_folder1, _ = MaterialFolder.objects.get_or_create(
            module=python_module1,
            name="Python Basics"
        )

        python_folder2, _ = MaterialFolder.objects.get_or_create(
            module=python_module2,
            name="Django REST Framework"
        )

        database_folder1, _ = MaterialFolder.objects.get_or_create(
            module=database_module1,
            name="SQL Queries"
        )

        # --------------------------------------------------
        # 8. STUDY MATERIALS
        # --------------------------------------------------

        python_material1, _ = StudyMaterial.objects.get_or_create(
            folder=python_folder1,
            title="Python Variables & Data Types",
            defaults={
                "material_type": "PDF",
                "url": "https://example.com/python-variables"
            }
        )

        python_material2, _ = StudyMaterial.objects.get_or_create(
            folder=python_folder1,
            title="Python Functions",
            defaults={
                "material_type": "Video",
                "url": "https://example.com/python-functions"
            }
        )

        python_material3, _ = StudyMaterial.objects.get_or_create(
            folder=python_folder2,
            title="Building REST APIs with DRF",
            defaults={
                "material_type": "PDF",
                "url": "https://example.com/drf-api"
            }
        )

        database_material1, _ = StudyMaterial.objects.get_or_create(
            folder=database_folder1,
            title="SQL SELECT Queries",
            defaults={
                "material_type": "PDF",
                "url": "https://example.com/sql-select"
            }
        )

        database_material2, _ = StudyMaterial.objects.get_or_create(
            folder=database_folder1,
            title="SQL Joins",
            defaults={
                "material_type": "Video",
                "url": "https://example.com/sql-joins"
            }
        )

        # --------------------------------------------------
        # 9. LIVE SESSIONS
        # --------------------------------------------------

        now = timezone.now()

        LiveSession.objects.get_or_create(
            classroom=python_classroom,
            title="Introduction to Python",
            defaults={
                "scheduled_at": now + timedelta(days=1),
                "meeting_url": "https://meet.example.com/python-intro"
            }
        )

        LiveSession.objects.get_or_create(
            classroom=python_classroom,
            title="Django REST Framework",
            defaults={
                "scheduled_at": now + timedelta(days=3),
                "meeting_url": "https://meet.example.com/django-rest"
            }
        )

        LiveSession.objects.get_or_create(
            classroom=database_classroom,
            title="SQL Basics",
            defaults={
                "scheduled_at": now + timedelta(days=2),
                "meeting_url": "https://meet.example.com/sql-basics"
            }
        )

        # --------------------------------------------------
        # 10. ASSIGNMENTS
        # --------------------------------------------------

        assignment1, _ = Assignment.objects.get_or_create(
            course=python_course,
            title="Python Programming Exercise",
            defaults={
                "description": "Solve basic Python programming problems.",
                "due_date": now + timedelta(days=5),
                "published": True
            }
        )

        assignment2, _ = Assignment.objects.get_or_create(
            course=python_course,
            title="Build a Django REST API",
            defaults={
                "description": "Create a REST API using Django REST Framework.",
                "due_date": now + timedelta(days=10),
                "published": True
            }
        )

        assignment3, _ = Assignment.objects.get_or_create(
            course=database_course,
            title="SQL Query Assignment",
            defaults={
                "description": "Write SQL queries using SELECT, JOIN and GROUP BY.",
                "due_date": now + timedelta(days=7),
                "published": True
            }
        )

        # --------------------------------------------------
        # 11. ASSIGNMENT SUBMISSIONS
        # --------------------------------------------------

        # Student 1 submitted assignment 1 but it is not evaluated yet
        AssignmentSubmission.objects.get_or_create(
            assignment=assignment1,
            student=student1,
            defaults={
                "submitted_at": now - timedelta(days=1)
            }
        )

        # Student 1 submitted and was evaluated for assignment 2
        AssignmentSubmission.objects.get_or_create(
            assignment=assignment2,
            student=student1,
            defaults={
                "submitted_at": now - timedelta(days=3),
                "evaluated_at": now - timedelta(days=2),
                "score": 92
            }
        )

        # Student 2 has submitted assignment 1
        AssignmentSubmission.objects.get_or_create(
            assignment=assignment1,
            student=student2,
            defaults={
                "submitted_at": now - timedelta(days=2)
            }
        )

        # --------------------------------------------------
        # 12. MATERIAL COMPLETION
        # --------------------------------------------------

        MaterialCompletion.objects.get_or_create(
            student=student1,
            material=python_material1,
            defaults={
                "completed": True,
                "completed_at": now - timedelta(days=2)
            }
        )

        MaterialCompletion.objects.get_or_create(
            student=student1,
            material=python_material2,
            defaults={
                "completed": True,
                "completed_at": now - timedelta(days=1)
            }
        )

        MaterialCompletion.objects.get_or_create(
            student=student2,
            material=python_material1,
            defaults={
                "completed": True,
                "completed_at": now - timedelta(days=1)
            }
        )

        self.stdout.write(
            self.style.SUCCESS("Seed data created successfully!")
        )
        self.stdout.write("")
        self.stdout.write("Student 1:")
        self.stdout.write("Username: rani")
        self.stdout.write("Password: Rani@12345")
        self.stdout.write("")
        self.stdout.write("Student 2:")
        self.stdout.write("Username: arun")
        self.stdout.write("Password: Arun@12345")