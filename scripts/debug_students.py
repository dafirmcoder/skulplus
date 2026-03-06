import os
import sys
import pathlib
# ensure project root is on sys.path so `config` and apps import correctly
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from schools.models import ClassRoom, Student, SubjectAllocation, HeadTeacher

User = get_user_model()

print('--- Environment check ---')
print('Users sample:', list(User.objects.values_list('username', flat=True)[:20]))

hts = HeadTeacher.objects.all()
print('HeadTeacher count:', hts.count())

for ht in hts:
    school = ht.school
    print('\nHeadteacher:', ht.user.username)
    print(' School:', school.name, 'id=', school.id)
    classes = ClassRoom.objects.filter(school=school)
    print(' Class count:', classes.count())
    for c in classes:
        cnt = Student.objects.filter(school=school, classroom=c).count()
        print(f"  Class {c.id} {c.name}: {cnt} students")

    total_students = Student.objects.filter(school=school).count()
    students_with_class = Student.objects.filter(school=school, classroom__isnull=False).count()
    print(' Total students:', total_students)
    print(' Students with classroom:', students_with_class)

    alloc_count = SubjectAllocation.objects.filter(student__school=school).count()
    print(' SubjectAllocation count:', alloc_count)
    sample_allocs = list(SubjectAllocation.objects.filter(student__school=school).values_list('student_id', 'subject_id')[:20])
    print(' Sample allocations (student_id,subject_id):', sample_allocs)

# Also list some students without classroom
orphan_students = Student.objects.filter(classroom__isnull=True)
print('\nStudents without classroom (sample 20):', list(orphan_students.values_list('id', 'first_name', 'last_name')[:20]))

print('\n--- End check ---')
