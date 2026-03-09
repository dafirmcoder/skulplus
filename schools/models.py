from django.db import models
from django.apps import apps
from typing import Any, cast
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .cbe import is_junior_subject_name, is_primary_subject_name


# 🏫 SCHOOL MODEL
class School(models.Model):
    SCHOOL_TYPES = (
        ('CAMBRIDGE', 'Cambridge'),
        ('CBE', 'CBE'),
    )

    SCHOOL_CATEGORY_CHOICES = (
        ('PRIMARY', 'Primary (Grades 1–6)'),
        ('JUNIOR', 'Junior (Grades 7–9)'),
        ('SENIOR', 'Senior (Grades 10–12)'),
        ('COMPREHENSIVE', 'Comprehensive (Primary + Junior)'),
    )

    name = models.CharField(max_length=255)
    motto = models.CharField(max_length=255, blank=True, default='')
    system_type = models.CharField(
        max_length=10,
        choices=[('844', '8-4-4'), ('CBE', 'Competency Based EDUCATION')],
        default='844'
    )
    school_category = models.CharField(
        max_length=20,
        choices=SCHOOL_CATEGORY_CHOICES,
        default='PRIMARY'
    )
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    stamp = models.ImageField(upload_to='school_stamps/', blank=True, null=True)
    head_signature = models.ImageField(upload_to='head_signatures/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.school_type})"

    def allows_level(self, level_name: str) -> bool:
        if self.system_type != 'CBE' or not level_name:
            return True
        category = self.school_category
        if category == 'PRIMARY':
            return level_name in ('Lower Primary', 'Upper Primary')
        if category == 'JUNIOR':
            return level_name == 'Junior'
        if category == 'SENIOR':
            return level_name == 'Senior'
        if category == 'COMPREHENSIVE':
            return level_name in ('Lower Primary', 'Upper Primary', 'Junior')
        return True

    def resolve_cbe_level(self, class_level_name=None):
        if self.system_type != 'CBE':
            return class_level_name
        category = self.school_category
        if category == 'PRIMARY':
            return class_level_name if class_level_name in ('Lower Primary', 'Upper Primary') else 'Lower Primary'
        if category == 'JUNIOR':
            return 'Junior'
        if category == 'SENIOR':
            return 'Senior'
        if category == 'COMPREHENSIVE':
            return class_level_name or 'Lower Primary'
        return class_level_name

    def allows_pathways(self) -> bool:
        return self.system_type == 'CBE' and self.school_category == 'SENIOR'


# 📘 SUBJECTS PER SCHOOL
class Subject(models.Model):
    SUBJECT_CATEGORY_STEM = 'STEM'
    SUBJECT_CATEGORY_SOCIAL_SCIENCES = 'SOCIAL_SCIENCES'
    SUBJECT_CATEGORY_ARTS_SPORTS_SCIENCE = 'ARTS_SPORTS_SCIENCE'
    SUBJECT_CATEGORY_CHOICES = (
        (SUBJECT_CATEGORY_STEM, 'STEM'),
        (SUBJECT_CATEGORY_SOCIAL_SCIENCES, 'Social Sciences'),
        (SUBJECT_CATEGORY_ARTS_SPORTS_SCIENCE, 'Arts & Sports Science'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects")
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30, null=True, blank=True)
    subject_category = models.CharField(max_length=30, choices=SUBJECT_CATEGORY_CHOICES, blank=True, default='')
    pathway = models.ForeignKey('Pathway', null=True, blank=True, on_delete=models.SET_NULL, related_name='school_subjects')
    education_level = models.ForeignKey('EducationLevel', on_delete=models.CASCADE, null=True, blank=True, related_name='school_subjects')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school', 'code', 'education_level'], name='unique_subject_code_per_school'),
            models.UniqueConstraint(fields=['school', 'name', 'education_level'], name='unique_subject_name_per_school'),
        ]

    def __str__(self):
        if self.short_name:
            return f"{self.code} - {self.name} ({self.short_name}) - {self.school.name}"
        return f"{self.code} - {self.name} - {self.school.name}"


class EducationLevel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Pathway(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


# 👨‍🏫 TEACHER MODEL
class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_class_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# Audit log for promotions/demotions
class PromotionLog(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    from_class = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    to_class = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} {self.from_class} -> {self.to_class} by {self.performed_by} at {self.timestamp}"


# 👨‍💼 HEADTEACHER (SCHOOL ADMIN)
class HeadTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='headteacher')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.school.name}"


class SchoolUserAccess(models.Model):
    ROLE_DEAN = 'DEAN'
    ROLE_SECRETARY = 'SECRETARY'
    ROLE_ACCOUNTS = 'ACCOUNTS'
    ROLE_DEPUTY = 'DEPUTY'
    ROLE_CHOICES = (
        (ROLE_DEAN, 'Dean'),
        (ROLE_SECRETARY, 'Secretary'),
        (ROLE_ACCOUNTS, 'Accounts (Bursar)'),
        (ROLE_DEPUTY, 'Deputy'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='user_access_roles')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school_access_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='granted_school_roles')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'School User Access Role'
        verbose_name_plural = 'School User Access Roles'

    def __str__(self):
        return f"{self.user.username} - {self.role} ({self.school.name})"


# 🏫 CLASSROOM MODEL
class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=100)  # e.g., Grade 1, Year 5
    section = models.CharField(max_length=50, blank=True)
    level = models.ForeignKey('EducationLevel', on_delete=models.CASCADE, null=True, blank=True)
    # Optional ordering index to allow sensible "previous/next" class navigation
    order = models.IntegerField(default=0)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_classes')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        if self.section:
            return f"{self.name} {self.section} - {self.school.name}"
        return f"{self.name} - {self.school.name}"


# 🌊 STREAM MODEL (e.g., Stream A, B, C within a classroom)
class Stream(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=50)  # e.g., "A", "B", "Science", "Arts"
    code = models.CharField(max_length=10)  # e.g., "STR_A", "STR_SCI"

    class Meta:
        unique_together = ('classroom', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.classroom.name} - Stream {self.name}"


# 👩‍🎓 STUDENT MODEL
class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    parent_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')))

    admission_number = models.CharField(max_length=50)
    admission_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school', 'admission_number'], name='unique_admission_per_school')
        ]

    parent_name = models.CharField(max_length=200, blank=True)
    parent_phone = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    is_alumni = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.school.name})"

    def total_fees_due(self, term, year):
        if not self.classroom_id:
            return 0

        FeeStructure = apps.get_model('finance', 'FeeStructure')
        structures = (
            FeeStructure.objects
            .filter(school=self.school, year=year, applicable_classes=self.classroom)
            .distinct()
        )

        total = 0
        for item in structures:
            if item.billing_mode == FeeStructure.BILLING_MODE_ONCE_YEAR:
                if item.due_term == term:
                    total += item.amount
            elif item.billing_mode == FeeStructure.BILLING_MODE_SELECTED_TERMS:
                if term in (item.applied_terms or []):
                    total += item.amount

        return total

    def total_paid(self, term, year):
        FeePayment = apps.get_model('finance', 'FeePayment')
        return FeePayment.objects.filter(student=self, term=term, year=year).aggregate(total=models.Sum('amount_paid'))['total'] or 0

    def balance(self, term, year):
        return self.total_fees_due(term, year) - self.total_paid(term, year)

# ANNOUNCEMENTS FOR PARENTS PORTAL
class Announcement(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 🎓 GRADE SCALE (FOR REPORT CARDS)
class GradeScale(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    min_score = models.FloatField()
    max_score = models.FloatField()
    grade = models.CharField(max_length=5)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score}) [{self.points}]"


# 🧾 EXAM RESULT SUMMARY PER TERM
class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    year = models.IntegerField()
    total_marks = models.FloatField()
    average = models.FloatField()
    position_in_class = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.term} {self.year}"


# Mapping of which students take which subjects
class SubjectAllocation(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='allocations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_allocations')
    # Snapshot of student's classroom and admission number at allocation time
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    admission_number = models.CharField(max_length=50, blank=True)
    # Snapshot of student's name at allocation time
    student_name = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('subject', 'student')

    def __str__(self):
        return f"{self.student} -> {self.subject}"

    def clean(self):
        super().clean()
        school = self.student.school
        if not school or school.system_type != 'CBE':
            return

        student_level_raw = self.student.classroom.level.name if self.student.classroom and self.student.classroom.level else None
        student_level = school.resolve_cbe_level(student_level_raw) if hasattr(school, 'resolve_cbe_level') else student_level_raw
        if student_level == 'Primary':
            class_name = self.student.classroom.name if self.student.classroom else ''
            match = re.search(r"(\d+)", class_name or '')
            if match:
                try:
                    grade = int(match.group(1))
                    if 1 <= grade <= 3:
                        student_level = 'Lower Primary'
                    elif 4 <= grade <= 6:
                        student_level = 'Upper Primary'
                except ValueError:
                    pass
        subject_level = self.subject.education_level.name if self.subject.education_level else None

        if student_level and not school.allows_level(student_level):
            raise ValidationError(f"This school is not configured for {student_level} classes.")

        if student_level == 'Senior':
            if not school.allows_pathways():
                raise ValidationError('Senior pathway features are disabled for this school.')
            try:
                from academics.models import StudentPathway
                pathway = StudentPathway.objects.filter(student=self.student).first()
            except Exception:
                pathway = None

            if not pathway:
                raise ValidationError('Senior students must select a pathway before subject registration.')

            if self.subject.pathway and pathway and cast(Any, pathway).pathway_id != cast(Any, self.subject).pathway_id:
                raise ValidationError('Senior students can only register subjects within their pathway.')

        if student_level == 'Junior':
            if subject_level != 'Junior':
                raise ValidationError('Junior students can only register Junior learning areas.')
            if not is_junior_subject_name(self.subject.name):
                raise ValidationError('This subject is not part of the Junior learning areas.')

        if student_level in ('Lower Primary', 'Upper Primary', 'Primary'):
            if subject_level not in (student_level, 'Primary'):
                raise ValidationError(f'{student_level} students can only register {student_level} learning areas.')
            if not is_primary_subject_name(self.subject.name):
                raise ValidationError('This subject is not part of the Primary learning areas.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


# Assignment of teachers to subjects and (optionally) classrooms and streams
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    # If stream is NULL, teacher teaches all streams in this class+subject

    class Meta:
        unique_together = ('teacher', 'subject', 'classroom', 'stream')

    def __str__(self):
        cls = f" ({self.classroom})" if self.classroom else ""
        return f"{self.teacher} -> {self.subject}{cls}"


# 🏫 STREAM CLASS TEACHER - Tracks class teacher per stream
class StreamClassTeacher(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='stream_class_teachers')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)  # Each classroom can have multiple streams
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('classroom', 'stream')

    def __str__(self):
        return f"{self.classroom} - {self.stream.name}: {self.teacher}"


# 📅 EXAM MODEL
class Exam(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)

    title = models.CharField(max_length=100)
    year = models.IntegerField()
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    marks_entry_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.year} {self.term})"


# 📆 TERM DATES PER SCHOOL
class TermDate(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='term_dates')
    year = models.IntegerField()
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('school', 'year', 'term')

    def __str__(self):
        return f"{self.school.name} {self.term} {self.year}: {self.start_date} - {self.end_date}"


# Site-level configuration (singleton pattern not enforced here; admin can keep one active entry)
class SiteConfig(models.Model):
    """Holds site-wide assets such as the logo uploaded by a superuser/admin.

    The templates use the most recently created SiteConfig if present.
    """
    site_name = models.CharField(max_length=200, default='SkulPlus')
    logo = models.ImageField(upload_to='site_logo/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site_logo/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return f"SiteConfig ({self.site_name})"


class MarkSheet(models.Model):
    term = models.CharField(max_length=20)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    school_class = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    out_of = models.IntegerField(default=100)

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'school_class', 'subject')

    def __str__(self):
        return f"{self.exam} - {self.school_class} - {self.subject}"


class StudentMark(models.Model):
    marksheet = models.ForeignKey(MarkSheet, related_name='marks', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    level = models.CharField(max_length=10, blank=True, default='')
    points = models.IntegerField(null=True, blank=True)
    comment_text = models.TextField(blank=True, default='')
    comment_manual = models.BooleanField(default=False)

    class Meta:
        unique_together = ('marksheet', 'student')


class CompetencyComment(models.Model):
    EDUCATION_LEVEL_CHOICES = (
        ('Primary', 'Primary'),
        ('Lower Primary', 'Lower Primary'),
        ('Upper Primary', 'Upper Primary'),
        ('Junior', 'Junior'),
    )

    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    subject = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL, related_name='competency_comments')
    performance_level = models.CharField(max_length=10)
    comment_text = models.TextField()

    class Meta:
        ordering = ['education_level', 'performance_level']

    def __str__(self):
        subject_name = self.subject.name if self.subject else 'General'
        return f"{self.education_level} {subject_name} {self.performance_level}"


