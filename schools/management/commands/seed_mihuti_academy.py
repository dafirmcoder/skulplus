import random
from datetime import date, timedelta
from collections import defaultdict
from typing import Any, cast

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from schools.models import (
    School, HeadTeacher, EducationLevel, ClassRoom, Stream, Subject,
    Teacher, TeacherAssignment, Student, SubjectAllocation,
    Exam, MarkSheet, StudentMark, CompetencyComment,
)
from schools.cbe import get_primary_level, get_junior_level


PRIMARY_SUBJECTS = [
    ("English", "ENG", "Eng"),
    ("Kiswahili", "KIS", "Kis"),
    ("Mathematics", "MATH", "Math"),
    ("Environmental / Science & Technology", "EST", "Env"),
    ("Social Studies", "SST", "Soc"),
    ("Religious Education", "RE", "RE"),
    ("Agriculture", "AGR", "Agr"),
    ("Creative Arts", "ART", "Art"),
    ("Physical & Health Education", "PHE", "PHE"),
    ("Life Skills", "LIFE", "Life"),
]

JUNIOR_SUBJECTS = [
    ("English", "ENG", "Eng"),
    ("Kiswahili", "KIS", "Kis"),
    ("Mathematics", "MATH", "Math"),
    ("Integrated Science", "ISCI", "Int Sci"),
    ("Health Education", "HLTH", "Health"),
    ("Social Studies", "SST", "Soc"),
    ("Religious Education", "RE", "RE"),
    ("Pre-Technical Studies", "PRET", "PreTech"),
    ("Business Studies", "BST", "Biz"),
    ("Agriculture", "AGR", "Agr"),
    ("Creative Arts", "CART", "Creat"),
    ("Sports & Physical Education", "SPE", "SPE"),
    ("Life Skills", "LIFE", "Life"),
]

STREAMS = ["North", "South", "East", "West"]
EXAM_TITLES = ["Opener", "Midterm", "Endterm"]
TERMS = ["Term 1", "Term 2", "Term 3"]

MALE_FIRST_NAMES = [
    "Brian", "Kevin", "Dennis", "Daniel", "Michael", "Joshua", "Ian", "Victor",
    "James", "Eric", "Joseph", "Samuel", "Peter", "Allan", "Collins", "Martin",
    "George", "Paul", "Ronald", "Felix",
]

FEMALE_FIRST_NAMES = [
    "Faith", "Grace", "Lilian", "Mary", "Susan", "Joy", "Angela", "Mercy",
    "Diana", "Catherine", "Lucy", "Irene", "Caroline", "Nancy", "Alice", "Janet",
    "Sheila", "Beatrice", "Esther", "Rose",
]

LAST_NAMES = [
    "Mwangi", "Njoroge", "Kiptoo", "Chebet", "Wanjiku", "Ochieng", "Odhiambo",
    "Kamau", "Kariuki", "Mutua", "Ngugi", "Achieng", "Kilonzo", "Wambui",
    "Cheruiyot", "Kiprotich", "Muli", "Wafula", "Barasa", "Juma",
]

TEACHER_NAMES = [
    ("Joseph", "Mwangi"),
    ("Mary", "Wanjiku"),
    ("Paul", "Kiprotich"),
    ("Grace", "Achieng"),
    ("Peter", "Kariuki"),
    ("Susan", "Njeri"),
    ("George", "Kamau"),
    ("Lucy", "Chebet"),
    ("Daniel", "Mutua"),
    ("Faith", "Wambui"),
    ("Brian", "Ochieng"),
    ("Catherine", "Kilonzo"),
    ("James", "Ngugi"),
    ("Irene", "Muli"),
    ("Samuel", "Barasa"),
    ("Joy", "Wafula"),
    ("Eric", "Odhiambo"),
]


class Command(BaseCommand):
    help = "Seed a comprehensive CBC dataset for A.C.K Mihuti Academy"

    def handle(self, *args, **options):
        random.seed(42)
        User = get_user_model()
        now = timezone.now().date()
        current_year = now.year
        years = [current_year - 1, current_year]

        summary = {
            "school_created": False,
            "teachers_created": 0,
            "students_created": 0,
            "classes_created": 0,
            "marks_generated": 0,
        }

        with transaction.atomic():
            school, created = School.objects.get_or_create(
                name="A.C.K Mihuti Academy",
                defaults={
                    "system_type": "CBE",
                    "school_type": "CBE",
                    "school_category": "COMPREHENSIVE",
                    "address": "P.O. Box 1024-00200, Nairobi, Kenya",
                    "motto": "Soar to Great Heights",
                },
            )
            if created:
                summary["school_created"] = True
            elif not school.motto:
                school.motto = "Soar to Great Heights"
                school.save(update_fields=["motto"])

            # Headteacher
            head_email = "sam@gmail.com"
            head_user = User.objects.filter(username=head_email).first()
            if not head_user:
                head_user = User.objects.create_user(
                    username=head_email,
                    email=head_email,
                    password="12345678",
                    first_name="Samson",
                    last_name="",
                )
            HeadTeacher.objects.get_or_create(
                user=head_user,
                defaults={
                    "school": school,
                    "full_name": "Samson",
                    "phone": "",
                },
            )

            # Education levels
            primary_level, _ = EducationLevel.objects.get_or_create(name="Primary")
            junior_level, _ = EducationLevel.objects.get_or_create(name="Junior")

            # Classes
            classes = []
            for grade in range(1, 7):
                for idx, stream in enumerate(STREAMS):
                    cls, was_created = ClassRoom.objects.get_or_create(
                        school=school,
                        name=f"Grade {grade}",
                        section=stream,
                        defaults={
                            "level": primary_level,
                            "order": grade * 10 + idx,
                        },
                    )
                    if was_created:
                        summary["classes_created"] += 1
                    else:
                        cls_obj = cast(Any, cls)
                        if not getattr(cls_obj, "level_id", None):
                            cls_obj.level = primary_level
                            cls_obj.save(update_fields=["level"])
                    classes.append(cls)

            for grade in range(7, 10):
                for idx, stream in enumerate(STREAMS):
                    cls, was_created = ClassRoom.objects.get_or_create(
                        school=school,
                        name=f"Grade {grade}",
                        section=stream,
                        defaults={
                            "level": junior_level,
                            "order": grade * 10 + idx,
                        },
                    )
                    if was_created:
                        summary["classes_created"] += 1
                    else:
                        cls_obj = cast(Any, cls)
                        if not getattr(cls_obj, "level_id", None):
                            cls_obj.level = junior_level
                            cls_obj.save(update_fields=["level"])
                    classes.append(cls)

            # Subjects
            subjects_primary = []
            for name, code, short in PRIMARY_SUBJECTS:
                subject, _ = Subject.objects.get_or_create(
                    school=school,
                    name=name,
                    defaults={"code": code, "short_name": short, "education_level": primary_level},
                )
                subject_obj = cast(Any, subject)
                if not getattr(subject_obj, "education_level_id", None):
                    subject_obj.education_level = primary_level
                    subject_obj.save(update_fields=["education_level"])
                subjects_primary.append(subject)

            subjects_junior = []
            for name, code, short in JUNIOR_SUBJECTS:
                subject, _ = Subject.objects.get_or_create(
                    school=school,
                    name=name,
                    defaults={"code": code, "short_name": short, "education_level": junior_level},
                )
                subject_obj = cast(Any, subject)
                if not getattr(subject_obj, "education_level_id", None):
                    subject_obj.education_level = junior_level
                    subject_obj.save(update_fields=["education_level"])
                subjects_junior.append(subject)

            # Teachers
            teachers = []
            for first, last in TEACHER_NAMES:
                email = f"{first.lower()}.{last.lower()}@ackmihuti.ac.ke"
                user = User.objects.filter(username=email).first()
                if not user:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password="12345678",
                        first_name=first,
                        last_name=last,
                    )
                teacher, was_created = Teacher.objects.get_or_create(
                    user=user,
                    defaults={"school": school},
                )
                if was_created:
                    summary["teachers_created"] += 1
                teacher_obj = cast(Any, teacher)
                school_obj = cast(Any, school)
                if getattr(teacher_obj, "school_id", None) != getattr(school_obj, "id", None):
                    teacher_obj.school = school
                    teacher_obj.save(update_fields=["school"])
                teachers.append(teacher)

            # Assign class teachers
            for idx, cls in enumerate(sorted(classes, key=lambda c: (c.name, c.section))):
                teacher = teachers[idx % len(teachers)]
                cls.class_teacher = teacher
                cls.save(update_fields=["class_teacher"])
                teacher.is_class_teacher = True
                teacher.save(update_fields=["is_class_teacher"])

            # Teacher subject assignments
            subject_teacher_map = {}
            subject_pool = subjects_primary + subjects_junior
            for idx, subject in enumerate(subject_pool):
                subject_teacher_map[subject.id] = teachers[idx % len(teachers)]

            assignment_batch = []
            for cls in classes:
                level = cls.level.name if cls.level else ""
                subjects_for_class = subjects_primary if level == "Primary" else subjects_junior
                for subject in subjects_for_class:
                    teacher = subject_teacher_map[subject.id]
                    assignment_batch.append(
                        TeacherAssignment(teacher=teacher, subject=subject, classroom=cls)
                    )
            TeacherAssignment.objects.bulk_create(assignment_batch, ignore_conflicts=True)

            # Students
            existing_admissions = set(
                Student.objects.filter(school=school).values_list('admission_number', flat=True)
            )
            seq = 1
            new_students = []
            for cls in classes:
                current_count = Student.objects.filter(school=school, classroom=cls).count()
                to_create = max(0, 37 - current_count)
                if to_create == 0:
                    continue

                grade_num = int(cls.name.split()[-1])
                base_age = 5 + grade_num
                for _ in range(to_create):
                    gender = "Male" if random.random() < 0.5 else "Female"
                    first = random.choice(MALE_FIRST_NAMES if gender == "Male" else FEMALE_FIRST_NAMES)
                    last = random.choice(LAST_NAMES)
                    while True:
                        admission_number = f"ACKM{seq:05d}"
                        seq += 1
                        if admission_number not in existing_admissions:
                            existing_admissions.add(admission_number)
                            break
                    age = base_age + random.choice([0, 1])
                    dob = now - timedelta(days=age * 365 + random.randint(0, 200))
                    new_students.append(
                        Student(
                            school=school,
                            classroom=cls,
                            stream=None,
                            first_name=first,
                            last_name=last,
                            date_of_birth=dob,
                            gender=gender,
                            admission_number=admission_number,
                            admission_date=now,
                            parent_name="",
                            parent_phone="",
                        )
                    )

            Student.objects.bulk_create(new_students, batch_size=500)
            summary["students_created"] += len(new_students)

            # Subject allocations
            class_students = defaultdict(list)
            for student in Student.objects.filter(school=school).select_related('classroom__level'):
                classroom_obj = cast(Any, student.classroom) if student.classroom else None
                classroom_id = getattr(student, "classroom_id", None) or (getattr(classroom_obj, "id", None) if classroom_obj else None)
                if classroom_id:
                    class_students[classroom_id].append(student)

            alloc_batch = []
            for cls in classes:
                level = cls.level.name if cls.level else ""
                subjects_for_class = subjects_primary if level == "Primary" else subjects_junior
                for student in class_students.get(cls.id, []):
                    for subject in subjects_for_class:
                        alloc_batch.append(
                            SubjectAllocation(
                                subject=subject,
                                student=student,
                                classroom=cls,
                                stream=None,
                                admission_number=student.admission_number,
                                student_name=f"{student.first_name} {student.last_name}",
                            )
                        )
            SubjectAllocation.objects.bulk_create(alloc_batch, batch_size=1000, ignore_conflicts=True)

            # Exams
            exams = []
            for year in years:
                for term in TERMS:
                    for title in EXAM_TITLES:
                        exam, _ = Exam.objects.get_or_create(
                            school=school,
                            title=title,
                            term=term,
                            year=year,
                            defaults={
                                "start_date": date(year, 1, 1),
                                "end_date": date(year, 1, 7),
                            },
                        )
                        exams.append(exam)

            # MarkSheets
            marksheet_batch = []
            existing_ms = set(
                MarkSheet.objects.filter(exam__in=exams, school_class__in=classes)
                .values_list('exam_id', 'school_class_id', 'subject_id')
            )
            for exam in exams:
                for cls in classes:
                    level = cls.level.name if cls.level else ""
                    subjects_for_class = subjects_primary if level == "Primary" else subjects_junior
                    for subject in subjects_for_class:
                        key = (exam.id, cls.id, subject.id)
                        if key in existing_ms:
                            continue
                        marksheet_batch.append(
                            MarkSheet(
                                exam=exam,
                                school_class=cls,
                                subject=subject,
                                term=exam.term,
                                out_of=100,
                                status='published',
                                created_by=head_user,
                            )
                        )
            MarkSheet.objects.bulk_create(marksheet_batch, batch_size=500, ignore_conflicts=True)

            # Reload marksheets for mark generation
            marksheets = list(
                MarkSheet.objects.filter(exam__in=exams, school_class__in=classes)
                .select_related('school_class__level', 'subject', 'exam')
            )

            # Comment cache
            comments_by_key = defaultdict(list)
            for comment in CompetencyComment.objects.all().select_related('subject'):
                key = (
                    comment.education_level,
                    getattr(comment, "subject_id", None),
                    comment.performance_level,
                )
                comments_by_key[key].append(comment.comment_text)

            last_comment = {}
            last_term = {}

            def pick_comment(level_name, subject_id, performance_level, student_id, term):
                specific_key = (level_name, subject_id, performance_level)
                general_key = (level_name, None, performance_level)
                options = comments_by_key.get(specific_key) or comments_by_key.get(general_key) or []
                if not options:
                    return ""
                prev = last_comment.get((student_id, subject_id))
                prev_term = last_term.get((student_id, subject_id))
                candidates = options
                if prev and prev_term and prev_term != term and len(options) > 1:
                    candidates = [c for c in options if c != prev] or options
                chosen = random.choice(candidates)
                last_comment[(student_id, subject_id)] = chosen
                last_term[(student_id, subject_id)] = term
                return chosen

            # Marks generation
            marks_to_create = []
            for exam in sorted(exams, key=lambda e: (e.year, TERMS.index(e.term), EXAM_TITLES.index(e.title))):
                exam_id = getattr(exam, "id", None)
                exam_marksheets = [m for m in marksheets if getattr(m, "exam_id", None) == exam_id]
                for ms in exam_marksheets:
                    students_in_class = class_students.get(getattr(ms, "school_class_id", None), [])
                    level_name = ms.school_class.level.name if ms.school_class.level else ""
                    for student in students_in_class:
                        score = max(0, min(100, random.gauss(65, 15)))
                        score = round(score, 1)
                        percentage = score
                        performance = (
                            get_primary_level(percentage) if level_name == "Primary" else get_junior_level(percentage)
                        )
                        comment_text = ""
                        if performance:
                            comment_text = pick_comment(level_name, getattr(ms, "subject_id", None), performance, student.id, ms.term)
                        marks_to_create.append(
                            StudentMark(
                                marksheet=ms,
                                student=student,
                                score=score,
                                comment_text=comment_text,
                            )
                        )

                        if len(marks_to_create) >= 2000:
                            StudentMark.objects.bulk_create(marks_to_create, batch_size=1000, ignore_conflicts=True)
                            summary["marks_generated"] += len(marks_to_create)
                            marks_to_create = []

            if marks_to_create:
                StudentMark.objects.bulk_create(marks_to_create, batch_size=1000, ignore_conflicts=True)
                summary["marks_generated"] += len(marks_to_create)

        self.stdout.write(self.style.SUCCESS("Seeding completed."))
        self.stdout.write(f"School created: {summary['school_created']}")
        self.stdout.write(f"Teachers created: {summary['teachers_created']}")
        self.stdout.write(f"Students created: {summary['students_created']}")
        self.stdout.write(f"Classes created: {summary['classes_created']}")
        self.stdout.write(f"Marks generated: {summary['marks_generated']}")
