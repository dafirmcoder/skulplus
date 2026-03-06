from django.db import models
from django.core.exceptions import ValidationError
from schools.models import Student, ClassRoom, School, EducationLevel, Pathway


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_subjects', null=True, blank=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    pathway = models.ForeignKey(Pathway, null=True, blank=True, on_delete=models.SET_NULL, related_name='academic_subjects')
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True, related_name='academic_subjects')

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class StudentPathway(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} -> {self.pathway.code}"

    def clean(self):
        super().clean()
        school = self.student.school
        if not school or school.system_type != 'CBE':
            raise ValidationError('Pathway selection is only allowed for CBE schools.')

        if hasattr(school, 'allows_pathways') and not school.allows_pathways():
            raise ValidationError('Pathway selection is disabled for this school.')

        level = self.student.classroom.level.name if self.student.classroom and self.student.classroom.level else None
        if hasattr(school, 'resolve_cbe_level'):
            level = school.resolve_cbe_level(level)
        if level != 'Senior':
            raise ValidationError('Pathway selection is only allowed for Senior level students.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Exam(models.Model):
    TERM_CHOICES = (
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.classroom} - {self.term} {self.year}"


class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    score = models.FloatField()

    class Meta:
        unique_together = ('exam', 'student', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.date}"
