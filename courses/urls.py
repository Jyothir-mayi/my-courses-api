from django.urls import path
from .views import CourseListView,CourseDetailView,MaterialCompletionView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path(
        'materials/<int:material_id>/completion/',
        MaterialCompletionView.as_view(),
        name='material-completion'
    ),
]
