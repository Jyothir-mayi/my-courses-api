from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import (
    Enrollment,
    Course,
    AssignmentSubmission,
    MaterialCompletion,
    StudyMaterial,
    Module,
    MaterialFolder,
)
from django.db.models import Prefetch
from django.utils import timezone

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('course', 'classroom')

        courses = []

        for enrollment in enrollments:
            courses.append({
                "id": enrollment.course.id,
                "name": enrollment.course.name,
                "description": enrollment.course.description,
                "classroom": (
                    enrollment.classroom.name
                    if enrollment.classroom
                    else None
                ),
            })

        return Response(courses)


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        # Make sure this student is enrolled in this course
        modules_queryset = Module.objects.order_by('order').prefetch_related(
            Prefetch(
                'folders',
                queryset=MaterialFolder.objects.prefetch_related('materials')
            )
        )

        enrollment = get_object_or_404(
            Enrollment.objects
            .select_related(
                'course',
                'classroom'
            )
            .prefetch_related(
                'classroom__faculty',
                'classroom__live_sessions',
                Prefetch(
                    'course__modules',
                    queryset=modules_queryset
                ),
                'course__assignments',
            ),
            student=request.user,
            course_id=course_id
        )

        course = enrollment.course
        classroom = enrollment.classroom

        # Load faculty and live sessions
        faculty = []
        live_sessions = []

        if classroom:
            faculty = [
                {
                    "id": member.id,
                    "name": member.name,
                    "email": member.email,
                }
                for member in classroom.faculty.all()
            ]

            live_sessions = [
                {
                    "id": session.id,
                    "title": session.title,
                    "scheduled_at": session.scheduled_at,
                    "meeting_url": session.meeting_url,
                }
                for session in classroom.live_sessions.all()
            ]

        # Load modules, folders and materials efficiently
        modules = []

        all_material_ids = []

        for module in course.modules.all():

            folders = []

            for folder in module.folders.all():

                materials = []

                for material in folder.materials.all():

                    all_material_ids.append(material.id)

                    materials.append({
                        "id": material.id,
                        "title": material.title,
                        "material_type": material.material_type,
                        "url": material.url,
                    })

                folders.append({
                    "id": folder.id,
                    "name": folder.name,
                    "materials": materials,
                })

            modules.append({
                "id": module.id,
                "title": module.title,
                "order": module.order,
                "folders": folders,
            })

        # Fetch all completion records for this student at once
        completions = MaterialCompletion.objects.filter(
            student=request.user,
            material_id__in=all_material_ids
        )

        completion_map = {
            completion.material_id: completion.completed
            for completion in completions
        }

        # Add completion status to each material
        total_materials = 0
        completed_materials = 0

        for module in modules:
            for folder in module["folders"]:
                for material in folder["materials"]:

                    is_completed = completion_map.get(
                        material["id"],
                        False
                    )

                    material["completed"] = is_completed

                    total_materials += 1

                    if is_completed:
                        completed_materials += 1

        # Load assignments
        assignments = list(course.assignments.all())

        assignment_ids = [
            assignment.id
            for assignment in assignments
        ]

        # Fetch all submissions for this student at once
        submissions = AssignmentSubmission.objects.filter(
            student=request.user,
            assignment_id__in=assignment_ids
        )

        submission_map = {
            submission.assignment_id: submission
            for submission in submissions
        }

        assignment_data = []

        for assignment in assignments:

            submission = submission_map.get(assignment.id)

            if not assignment.published:
                status = "not_published"
            elif submission and submission.evaluated_at:
                status = "evaluated"
            elif submission and submission.submitted_at:
                status = "submitted"
            else:
                status = "published"

            assignment_data.append({
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "due_date": assignment.due_date,
                "status": status,
                "submitted_at": (
                    submission.submitted_at
                    if submission
                    else None
                ),
                "evaluated_at": (
                    submission.evaluated_at
                    if submission
                    else None
                ),
                "score": (
                    submission.score
                    if submission
                    else None
                ),
            })

        # Calculate course progress
        progress = (
            round(
                (completed_materials / total_materials) * 100,
                2
            )
            if total_materials > 0
            else 0
        )

        return Response({
            "id": course.id,
            "name": course.name,
            "description": course.description,

            "classroom": (
                {
                    "id": classroom.id,
                    "name": classroom.name,
                }
                if classroom
                else None
            ),

            "faculty": faculty,
            "live_sessions": live_sessions,
            "modules": modules,
            "assignments": assignment_data,

            "progress": {
                "completed_materials": completed_materials,
                "total_materials": total_materials,
                "percentage": progress,
            },
        })
    

class MaterialCompletionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, material_id):

        # Find the material
        material = get_object_or_404(
            StudyMaterial.objects.select_related(
                'folder__module__course'
            ),
            id=material_id
        )

        # Get the course containing this material
        course = material.folder.module.course

        # Make sure the current student is enrolled in this course
        enrollment_exists = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

        if not enrollment_exists:
            return Response(
                {"detail": "You are not enrolled in this course."},
                status=403
            )

        # Validate the completed value
        if "completed" not in request.data:
            return Response(
                {"detail": "The 'completed' field is required."},
                status=400
            )

        completed = request.data["completed"]

        if not isinstance(completed, bool):
            return Response(
                {"detail": "'completed' must be true or false."},
                status=400
            )

        # Create or update this student's completion record
        completion, created = MaterialCompletion.objects.update_or_create(
            student=request.user,
            material=material,
            defaults={
                "completed": completed,
                "completed_at": timezone.now() if completed else None,
            }
        )

        return Response({
            "material_id": material.id,
            "completed": completion.completed,
            "completed_at": completion.completed_at,
        })