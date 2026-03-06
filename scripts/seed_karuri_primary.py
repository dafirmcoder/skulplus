"""Seed Karuri Primary School with demo classes, subjects, students, and grade scales.

Run with: python scripts/seed_karuri_primary.py
"""
import os
import sys
import random
from datetime import date, timedelta

# Ensure project root on sys.path before importing Django settings
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.db import transaction

from django.contrib.auth.models import User

from schools.models import (
    ClassRoom,
    GradeScale,
    School,
    Student,
    Subject,
    Stream,
    Teacher,
    TeacherAssignment,
    SubjectAllocation,
    Exam,
    MarkSheet,
    StudentMark,
)

SCHOOL_NAME = 'Karuri Primary'
SUBJECT_DATA = [
    ('ENG', 'English', 'ENG'),
    ('KIS', 'Kiswahili', 'KIS'),
    ('MAT', 'Mathematics', 'MATH'),
    ('SCI', 'Science', 'SCI'),
    ('SST', 'Social Studies', 'SST'),
    ('CRE', 'Christian Religious Education', 'CRE'),
    ('ART', 'Creative Arts', 'ART'),
    ('PE', 'Physical Education', 'PE'),
    ('LIT', 'Literature & Reading', 'LIT'),
    ('ICT', 'Computer Studies', 'ICT'),
    ('AGR', 'Agriculture', 'AGR'),
    ('MUS', 'Music', 'MUS'),
    ('LFE', 'Life Skills', 'LIFE'),
    ('CIV', 'Civic Education', 'CIV'),
    ('FRE', 'French Club', 'FRE'),
]
STREAM_NAMES = ['A', 'B', 'C']
EXAMS_BY_TERM = {
    'Term 1': 'End Term 1',
    'Term 2': 'End Term 2',
    'Term 3': 'End Term 3',
}
MARK_OUT_OF = 100
OVERWRITE_MARKS = False
GRADE_BANDS = [
    (80, 100, 'A'),
    (75, 79, 'A-'),
    (70, 74, 'B+'),
    (65, 69, 'B'),
    (60, 64, 'B-'),
    (55, 59, 'C+'),
    (50, 54, 'C'),
    (45, 49, 'C-'),
    (40, 44, 'D+'),
    (35, 39, 'D'),
    (0, 34, 'D-'),
]
FIRST_NAMES = [
    'Amani', 'Brenda', 'Caleb', 'Diana', 'Elsie', 'Farid', 'Grace', 'Hassan', 'Ivy', 'Joel',
    'Kevin', 'Linda', 'Morris', 'Naomi', 'Oscar', 'Pendo', 'Quinn', 'Riley', 'Susan', 'Tariq',
]
LAST_NAMES = [
    'Kamau', 'Wambui', 'Mwangi', 'Njeri', 'Ochieng', 'Otieno', 'Mutua', 'Achieng', 'Kariuki',
    'Chebet', 'Barasa', 'Amollo', 'Korir', 'Cherono', 'Nyambura', 'Anyango', 'Muriithi', 'Maina',
    'Ngugi', 'Omondi',
]


def ensure_school():
    defaults = {
        'school_type': 'CBE',
        'address': 'Karuri, Kiambu County',
        'phone': '+254-700-000-000',
        'email': 'info@karuriprimary.sch.ke',
    }
    school, created = School.objects.update_or_create(name=SCHOOL_NAME, defaults=defaults)
    return school, created


def seed_classrooms(school):
    classrooms = []
    created_count = 0
    for order in range(1, 10):
        name = f'Grade {order}'
        classroom, created = ClassRoom.objects.update_or_create(
            school=school,
            name=name,
            defaults={
                'section': '',
                'order': order,
                'class_teacher': None,
            },
        )
        classrooms.append((order, classroom))
        if created:
            created_count += 1
    return classrooms, created_count


def seed_subjects(school):
    created_count = 0
    for code, name, short_name in SUBJECT_DATA:
        _, created = Subject.objects.update_or_create(
            school=school,
            code=code,
            defaults={'name': name, 'short_name': short_name},
        )
        if created:
            created_count += 1
    return created_count


def seed_grade_scale(school):
    GradeScale.objects.filter(school=school).delete()
    GradeScale.objects.bulk_create(
        [GradeScale(school=school, min_score=low, max_score=high, grade=grade) for low, high, grade in GRADE_BANDS]
    )
    return len(GRADE_BANDS)


def seed_students(school, classrooms):
    base_admission = date(2024, 1, 10)
    created_count = 0
    updated_count = 0

    for order, classroom in classrooms:
        for index in range(1, 31):
            admission_number = f'KAR{order:02d}{index:03d}'
            first_name = FIRST_NAMES[(index - 1) % len(FIRST_NAMES)]
            last_name = LAST_NAMES[(order + index - 2) % len(LAST_NAMES)]
            gender = 'Male' if (order + index) % 2 == 0 else 'Female'
            birth_year = 2018 - (order - 1)
            month = ((index - 1) % 12) + 1
            day = ((index - 1) % 28) + 1
            dob = date(birth_year, month, day)
            admission_date = base_admission + timedelta(days=((order - 1) * 15) + index)
            parent_name = f'{last_name} Household'
            parent_phone = f'+2547{order}{index:04d}'

            defaults = {
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'classroom': classroom,
                'date_of_birth': dob,
                'admission_date': admission_date,
                'parent_name': parent_name,
                'parent_phone': parent_phone,
                'is_alumni': False,
            }

            student, created = Student.objects.update_or_create(
                school=school,
                admission_number=admission_number,
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

    return created_count, updated_count


def seed_streams(classrooms):
    created_count = 0
    streams_map = {}
    for _, classroom in classrooms:
        streams_map[classroom.id] = []
        for idx, name in enumerate(STREAM_NAMES, start=1):
            code = f"STR_{name}_{classroom.id}"
            stream, created = Stream.objects.update_or_create(
                classroom=classroom,
                name=name,
                defaults={'code': code},
            )
            streams_map[classroom.id].append(stream)
            if created:
                created_count += 1
    return streams_map, created_count


def assign_students_to_streams(school, classrooms, streams_map):
    updated = 0
    for _, classroom in classrooms:
        students = list(Student.objects.filter(school=school, classroom=classroom).order_by('admission_number'))
        streams = streams_map.get(classroom.id, [])
        if not streams:
            continue
        for idx, student in enumerate(students):
            stream = streams[idx % len(streams)]
            if student.stream_id != stream.id:
                student.stream = stream
                student.save(update_fields=['stream'])
                updated += 1
    return updated


def seed_teachers(school, count=12):
    created = 0
    teachers = []
    for i in range(1, count + 1):
        email = f"teacher{i}@karuri.local"
        user, user_created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': f"Teacher{i}",
                'last_name': "Karuri",
            },
        )
        if user_created:
            user.set_password('Pass1234!')
            user.save(update_fields=['password'])

        teacher, teacher_created = Teacher.objects.get_or_create(school=school, user=user)
        if teacher_created:
            created += 1
        teachers.append(teacher)
    return teachers, created


def assign_class_teachers(classrooms, teachers):
    updated = 0
    if not teachers:
        return updated
    for idx, (_, classroom) in enumerate(classrooms):
        teacher = teachers[idx % len(teachers)]
        if classroom.class_teacher_id != teacher.id:
            classroom.class_teacher = teacher
            classroom.save(update_fields=['class_teacher'])
            updated += 1
    return updated


def seed_teacher_assignments(classrooms, subjects, teachers, streams_map):
    created = 0
    if not teachers:
        return created
    for _, classroom in classrooms:
        class_teachers = teachers[:]
        random.shuffle(class_teachers)
        for idx, subject in enumerate(subjects):
            teacher = class_teachers[idx % len(class_teachers)]
            stream = None
            # Randomly assign a stream-specific teacher sometimes
            if streams_map.get(classroom.id) and idx % 3 == 0:
                stream = random.choice(streams_map[classroom.id])
            _, created_flag = TeacherAssignment.objects.get_or_create(
                teacher=teacher,
                subject=subject,
                classroom=classroom,
                stream=stream,
            )
            if created_flag:
                created += 1
    return created


def seed_subject_allocations(school, classrooms, subjects):
    created = 0
    for _, classroom in classrooms:
        students = Student.objects.filter(school=school, classroom=classroom)
        for student in students:
            for subject in subjects:
                _, created_flag = SubjectAllocation.objects.get_or_create(
                    subject=subject,
                    student=student,
                    defaults={
                        'classroom': student.classroom,
                        'stream': student.stream,
                        'admission_number': student.admission_number,
                        'student_name': f"{student.first_name} {student.last_name}",
                    },
                )
                if created_flag:
                    created += 1
    return created


def seed_exams(school, year):
    created = 0
    exams = []
    for term, title in EXAMS_BY_TERM.items():
        start_date = date(year, 1, 15) if term == 'Term 1' else date(year, 5, 15) if term == 'Term 2' else date(year, 9, 15)
        end_date = start_date + timedelta(days=30)
        exam, created_flag = Exam.objects.update_or_create(
            school=school,
            title=title,
            year=year,
            term=term,
            defaults={'start_date': start_date, 'end_date': end_date},
        )
        exams.append(exam)
        if created_flag:
            created += 1
    return exams, created


def generate_score():
    pct = random.gauss(62, 12)
    pct = max(30, min(95, pct))
    return round((MARK_OUT_OF * pct) / 100.0, 1)


def seed_marks(school, classrooms, subjects, exams):
    marksheets_created = 0
    marks_created = 0
    marks_updated = 0
    marks_skipped = 0

    for exam in exams:
        for _, classroom in classrooms:
            for subject in subjects:
                marksheet, created = MarkSheet.objects.get_or_create(
                    exam=exam,
                    school_class=classroom,
                    subject=subject,
                    defaults={
                        'term': exam.term,
                        'out_of': MARK_OUT_OF,
                        'status': 'published',
                        'created_by': None,
                    },
                )
                if created:
                    marksheets_created += 1

                students = Student.objects.filter(school=school, classroom=classroom)
                for student in students:
                    score = generate_score()
                    mark_obj, created_mark = StudentMark.objects.get_or_create(
                        marksheet=marksheet,
                        student=student,
                        defaults={'score': score},
                    )
                    if created_mark:
                        marks_created += 1
                    else:
                        if OVERWRITE_MARKS or mark_obj.score is None:
                            mark_obj.score = score
                            mark_obj.save(update_fields=['score'])
                            marks_updated += 1
                        else:
                            marks_skipped += 1

    return marksheets_created, marks_created, marks_updated, marks_skipped


@transaction.atomic
def main():
    school, school_created = ensure_school()
    classrooms, classes_created = seed_classrooms(school)
    subjects_created = seed_subjects(school)
    grade_rows = seed_grade_scale(school)
    students_created, students_updated = seed_students(school, classrooms)
    streams_map, streams_created = seed_streams(classrooms)
    students_streamed = assign_students_to_streams(school, classrooms, streams_map)
    teachers, teachers_created = seed_teachers(school)
    class_teachers_updated = assign_class_teachers(classrooms, teachers)
    assignments_created = seed_teacher_assignments(classrooms, Subject.objects.filter(school=school), teachers, streams_map)
    allocations_created = seed_subject_allocations(school, classrooms, Subject.objects.filter(school=school))
    exams, exams_created = seed_exams(school, date.today().year)
    marksheets_created, marks_created, marks_updated, marks_skipped = seed_marks(
        school,
        classrooms,
        Subject.objects.filter(school=school),
        exams,
    )

    print('--- Karuri Primary Seed Complete ---')
    print(f"School: {school.name} ({'created' if school_created else 'updated'})")
    print(f'Classrooms ensured: {len(classrooms)} (new: {classes_created})')
    print(f'Subjects ensured: {len(SUBJECT_DATA)} (new: {subjects_created})')
    print(f'Grade bands reset: {grade_rows}')
    print(
        f'Students processed: {len(classrooms) * 30} '
        f'(created: {students_created}, updated: {students_updated})'
    )
    print(f'Streams ensured: {len(classrooms) * len(STREAM_NAMES)} (new: {streams_created})')
    print(f'Students assigned to streams: {students_streamed}')
    print(f'Teachers ensured: {len(teachers)} (new: {teachers_created})')
    print(f'Class teachers updated: {class_teachers_updated}')
    print(f'Teacher assignments created: {assignments_created}')
    print(f'Subject allocations created: {allocations_created}')
    print(f'Exams ensured: {len(exams)} (new: {exams_created})')
    print(f'MarkSheets created: {marksheets_created}')
    print(f'Marks created: {marks_created}, updated: {marks_updated}, skipped: {marks_skipped}')


if __name__ == '__main__':
    main()
