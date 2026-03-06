from __future__ import annotations

from datetime import date
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from schools.cbe import ensure_cbe_learning_areas
from schools.models import (
    ClassRoom,
    EducationLevel,
    Exam,
    HeadTeacher,
    School,
    Stream,
    Student,
    Subject,
    SubjectAllocation,
    Teacher,
    TeacherAssignment,
)


class Command(BaseCommand):
    help = "Seed Darfim Tuition Centre with demo data"

    def handle(self, *args, **options):
        User = get_user_model()
        current_year = date.today().year

        with transaction.atomic():
            school, _ = School.objects.get_or_create(
                name="Darfim Tuition Centre",
                defaults={
                    "system_type": "CBE",
                    "school_type": "CBE",
                    "school_category": "PRIMARY",
                    "address": "Nairobi, Kenya",
                    "email": "info@darfimtuition.co.ke",
                    "phone": "+254700000000",
                    "motto": "Learn. Grow. Excel.",
                },
            )

            head_email = "admin@darfimtuition.co.ke"
            head_user, created_user = User.objects.get_or_create(
                username=head_email,
                defaults={
                    "email": head_email,
                    "first_name": "Darfim",
                    "last_name": "Admin",
                    "is_staff": True,
                },
            )
            if created_user:
                head_user.set_password("12345678")
                head_user.save(update_fields=["password"])

            HeadTeacher.objects.get_or_create(
                user=head_user,
                defaults={
                    "school": school,
                    "full_name": "Darfim Admin",
                    "phone": "+254700000000",
                },
            )

            lower_primary, _ = EducationLevel.objects.get_or_create(name="Lower Primary")
            upper_primary, _ = EducationLevel.objects.get_or_create(name="Upper Primary")

            ensure_cbe_learning_areas(school)
            subjects = list(
                Subject.objects.filter(school=school)
                .select_related("education_level")
            )

            classrooms: list[ClassRoom] = []
            for grade in range(1, 7):
                level = lower_primary if grade <= 3 else upper_primary
                classroom, _ = ClassRoom.objects.get_or_create(
                    school=school,
                    name=f"Grade {grade}",
                    section="",
                    defaults={"level": level, "order": grade},
                )
                if classroom.level_id != level.id:
                    classroom.level = level
                    classroom.save(update_fields=["level"])
                classrooms.append(classroom)

                for stream_name in ("A", "B"):
                    Stream.objects.get_or_create(
                        classroom=classroom,
                        name=stream_name,
                        defaults={"code": f"G{grade}{stream_name}"},
                    )

            teachers: list[Teacher] = []
            for i in range(1, 7):
                email = f"teacher{i}@darfimtuition.co.ke"
                u, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        "email": email,
                        "first_name": f"Teacher{i}",
                        "last_name": "Darfim",
                    },
                )
                if created:
                    u.set_password("12345678")
                    u.save(update_fields=["password"])
                teacher, _ = Teacher.objects.get_or_create(user=u, defaults={"school": school})
                if teacher.school_id != school.id:
                    teacher.school = school
                    teacher.save(update_fields=["school"])
                teachers.append(teacher)

            for idx, classroom in enumerate(classrooms):
                classroom.class_teacher = teachers[idx % len(teachers)]
                classroom.save(update_fields=["class_teacher"])

            for idx, classroom in enumerate(classrooms):
                class_level = classroom.level.name if classroom.level else ""
                class_subjects = [
                    s for s in subjects
                    if getattr(getattr(s, "education_level", None), "name", "") == class_level
                ]
                for s_idx, subject in enumerate(class_subjects):
                    TeacherAssignment.objects.get_or_create(
                        teacher=teachers[(idx + s_idx) % len(teachers)],
                        classroom=classroom,
                        subject=subject,
                        stream=None,
                    )

            first_names = [
                "Faith", "Brian", "Joy", "Kevin", "Grace", "Mercy", "Ian", "Lucy",
                "Daniel", "Rose", "Paul", "Mary", "Peter", "Alice", "John", "Esther",
            ]
            last_names = [
                "Mwangi", "Achieng", "Otieno", "Kariuki", "Njoroge", "Wanjiru", "Mutiso", "Kamau"
            ]

            created_students = 0
            for classroom in classrooms:
                streams = list(Stream.objects.filter(classroom=classroom).order_by("name"))
                class_level = classroom.level.name if classroom.level else ""
                class_subjects = [
                    s for s in subjects
                    if getattr(getattr(s, "education_level", None), "name", "") == class_level
                ]
                for n in range(1, 7):
                    stream = streams[(n - 1) % len(streams)] if streams else None
                    admission = f"DTC{classroom.name.replace('Grade ', '')}{n:03d}"
                    student, was_created = Student.objects.get_or_create(
                        school=school,
                        admission_number=admission,
                        defaults={
                            "classroom": classroom,
                            "stream": stream,
                            "first_name": first_names[(n - 1) % len(first_names)],
                            "last_name": last_names[(n - 1) % len(last_names)],
                            "gender": "Male" if n % 2 else "Female",
                            "admission_date": date(current_year, 1, 10),
                        },
                    )
                    if not was_created:
                        updates = []
                        if student.classroom_id != classroom.id:
                            student.classroom = classroom
                            updates.append("classroom")
                        if stream and student.stream_id != stream.id:
                            student.stream = stream
                            updates.append("stream")
                        if updates:
                            student.save(update_fields=updates)
                    else:
                        created_students += 1

                    for subject in class_subjects:
                        SubjectAllocation.objects.get_or_create(
                            subject=subject,
                            student=student,
                            defaults={
                                "classroom": classroom,
                                "stream": stream,
                                "admission_number": student.admission_number,
                                "student_name": f"{student.first_name} {student.last_name}".strip(),
                            },
                        )

            for term in ("Term 1", "Term 2", "Term 3"):
                Exam.objects.get_or_create(
                    school=school,
                    title="Opener",
                    term=term,
                    year=current_year,
                    defaults={
                        "start_date": date(current_year, 2, 1),
                        "end_date": date(current_year, 2, 5),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Seeded Darfim Tuition Centre successfully."))
        self.stdout.write("Headteacher username: admin@darfimtuition.co.ke")
        self.stdout.write("Headteacher password: 12345678")
