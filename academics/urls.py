from django.urls import path
from .views import (
    lessonplan_generator,
    reports_dashboard,
    resources_dashboard,
    scheme_generator,
    syllabus_coverage,
    teacher_dashboard,
)

urlpatterns = [
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('schemes/', scheme_generator, name='scheme_generator'),
    path('lesson-plans/', lessonplan_generator, name='lessonplan_generator'),
    path('syllabus-coverage/', syllabus_coverage, name='syllabus_coverage'),
    path('resources/', resources_dashboard, name='academics_resources'),
    path('reports/', reports_dashboard, name='academics_reports'),
]
