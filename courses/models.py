from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Classroom(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )
    name = models.CharField(max_length=100)
    faculty = models.ManyToManyField(Faculty, related_name='classrooms')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class MaterialFolder(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='folders'
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class StudyMaterial(models.Model):
    folder = models.ForeignKey(
        MaterialFolder,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=50)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class LiveSession(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='live_sessions'
    )
    title = models.CharField(max_length=200)
    scheduled_at = models.DateTimeField()
    meeting_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class MaterialCompletion(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='material_completions'
    )
    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE,
        related_name='completions'
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'material'],
                name='unique_student_material'
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.material.title}"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignment_submissions'
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assignment', 'student'],
                name='unique_student_assignment'
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"