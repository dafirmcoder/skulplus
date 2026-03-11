from django.contrib import admin
from .models import (
    School, ClassRoom, Student, Subject, Stream,
    Teacher, HeadTeacher, Announcement,
    GradeScale, ExamResult, MarkSheet,
    StudentMark, CompetencyComment, EducationLevel,
    Pathway, PromotionLog, StreamClassTeacher, TermDate, SchoolTypePricing, LearningResource, Assignment
)
from .models import SiteConfig
from .models import Exam
from .models import SubjectAllocation
from .models import TeacherAssignment
from .models import SchoolUserAccess
def get_user_school(user):
    if hasattr(user, 'headteacher'):
        return user.headteacher.school
    return None


# 🏫 SCHOOL ADMIN
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type', 'system_type', 'school_category', 'student_limit', 'phone', 'email')


# 📘 SUBJECT ADMIN
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'short_name', 'school')
    list_filter = ('school',)
    search_fields = ('code', 'name', 'short_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusers should see all exams; headteachers see only their school
        if request.user.is_superuser:
            return qs
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs



# 👨‍🏫 TEACHER ADMIN
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'is_class_teacher')
    list_filter = ('school', 'is_class_teacher')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs
    
    def save_model(self, request, obj, form, change):
        # Ensure username matches email for teachers
        if obj.user and obj.user.email:
            obj.user.username = obj.user.email.lower()
            obj.user.save()
        super().save_model(request, obj, form, change)


# 👨‍💼 HEADTEACHER ADMIN
@admin.register(HeadTeacher)
class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')


# 🏫 CLASSROOM ADMIN
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'school', 'class_teacher')
    list_filter = ('school',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs


# 🌊 STREAM ADMIN
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'classroom')
    list_filter = ('classroom__school',)
    search_fields = ('name', 'code', 'classroom__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(classroom__school=school)
        return qs


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Pathway)
class PathwayAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


# 👩‍🎓 STUDENT ADMIN
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'classroom', 'stream', 'admission_number')
    list_filter = ('school', 'classroom', 'stream')
    search_fields = ('first_name', 'last_name', 'admission_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs


# 📢 ANNOUNCEMENTS ADMIN
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'created_at')
    list_filter = ('school',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs



# 🎓 GRADE SCALE ADMIN
@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('grade', 'min_score', 'max_score', 'school')
    list_filter = ('school',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs


@admin.register(TermDate)
class TermDateAdmin(admin.ModelAdmin):
    list_display = ('term', 'year', 'start_date', 'end_date', 'school')
    list_filter = ('year', 'term', 'school')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'term', 'start_date', 'end_date', 'school')
    list_filter = ('year', 'term', 'school')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs



# 🧾 EXAM RESULTS ADMIN
@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'year', 'average', 'position_in_class')
    list_filter = ('term', 'year')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(student__school=school)
        return qs


@admin.register(SubjectAllocation)
class SubjectAllocationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student')
    list_filter = ('subject',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(subject__school=school)
        return qs


@admin.register(StreamClassTeacher)
class StreamClassTeacherAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'stream', 'teacher')
    list_filter = ('classroom__school',)


@admin.register(PromotionLog)
class PromotionLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_class', 'to_class', 'performed_by', 'timestamp')
    list_filter = ('from_class__school',)
    search_fields = ('student__first_name', 'student__last_name', 'student__admission_number')


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'classroom')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(teacher__school=school)
        return qs


# Mark sheets show published exam entries; StudentMark lists the per-learner scores
@admin.register(MarkSheet)
class MarkSheetAdmin(admin.ModelAdmin):
    list_display = ('exam', 'school_class', 'subject', 'term', 'status', 'created_at')
    list_filter = ('status', 'term', 'exam__year', 'school_class__school')
    search_fields = ('exam__title', 'subject__name', 'school_class__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(school_class__school=school)
        return qs


@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('marksheet', 'student', 'score', 'level', 'points')
    list_filter = ('marksheet__exam__year', 'marksheet__term', 'student__school')
    search_fields = ('student__first_name', 'student__last_name', 'marksheet__subject__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        school = get_user_school(request.user)
        if school:
            return qs.filter(student__school=school)
        return qs


@admin.register(CompetencyComment)
class CompetencyCommentAdmin(admin.ModelAdmin):
    list_display = ('education_level', 'performance_level', 'subject')
    list_filter = ('education_level', 'performance_level', 'subject')
    search_fields = ('comment_text',)


# Site configuration admin — superusers can upload/update the logo used across the site
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at')
    readonly_fields = ('updated_at',)
    def has_add_permission(self, request):
        # allow adding but keep it flexible; superusers can manage entries
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(SchoolUserAccess)
class SchoolUserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'role', 'is_active', 'updated_at')
    list_filter = ('school', 'role', 'is_active')


@admin.register(SchoolTypePricing)
class SchoolTypePricingAdmin(admin.ModelAdmin):
    list_display = ('school_type', 'price_per_student')


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'curriculum', 'resource_type', 'education_level', 'class_name', 'subject_name', 'is_active', 'created_at')
    list_filter = ('curriculum', 'resource_type', 'education_level', 'is_active')
    search_fields = ('title', 'description', 'class_name', 'subject_name')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'classroom', 'subject', 'term', 'year', 'teacher', 'created_at')
    list_filter = ('school', 'term', 'year', 'classroom', 'subject')
    search_fields = ('title', 'classroom__name', 'subject__name', 'teacher__user__first_name', 'teacher__user__last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        school = get_user_school(request.user)
        if school:
            return qs.filter(school=school)
        return qs


