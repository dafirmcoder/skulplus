from django.contrib import admin
from .models import Subject, StudentPathway, Exam, Mark, Attendance


@admin.register(Subject)
class AcademicSubjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'school', 'education_level', 'pathway')
	list_filter = ('school', 'education_level', 'pathway')
	search_fields = ('name', 'short_name')


@admin.register(StudentPathway)
class StudentPathwayAdmin(admin.ModelAdmin):
	list_display = ('student', 'pathway')
	list_filter = ('pathway',)
	search_fields = ('student__first_name', 'student__last_name', 'student__admission_number')


@admin.register(Exam)
class AcademicExamAdmin(admin.ModelAdmin):
	list_display = ('classroom', 'term', 'year', 'school')
	list_filter = ('term', 'year', 'school')


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
	list_display = ('student', 'subject', 'score', 'exam')
	list_filter = ('exam__year', 'exam__term', 'student__school')
	search_fields = ('student__first_name', 'student__last_name', 'subject__name')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('student', 'date', 'present')
	list_filter = ('date', 'present')
	search_fields = ('student__first_name', 'student__last_name', 'student__admission_number')
