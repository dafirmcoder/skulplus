import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from schools.models import School, HeadTeacher, ClassRoom, Student, Subject, SubjectAllocation

User = get_user_model()

def cleanup():
    school = School.objects.filter(name='Smoke School').first()
    user = User.objects.filter(username='smoke_head').first()

    if not school and not user:
        print('No smoke test data found.')
        return

    if school:
        sa_deleted = SubjectAllocation.objects.filter(student__school=school).delete()
        print('Deleted SubjectAllocation:', sa_deleted)

        subj_deleted = Subject.objects.filter(school=school, code='S1').delete()
        print('Deleted Subject:', subj_deleted)

        students_deleted = Student.objects.filter(school=school, admission_number__in=['S001','S002']).delete()
        print('Deleted Students:', students_deleted)

        classes_deleted = ClassRoom.objects.filter(school=school, name='SmokeClass', section='A').delete()
        print('Deleted ClassRoom:', classes_deleted)

        # remove headteacher link(s)
        ht_deleted = HeadTeacher.objects.filter(school=school, user__username='smoke_head').delete()
        print('Deleted HeadTeacher entries:', ht_deleted)

        # attempt to delete school if empty
        remaining = (Subject.objects.filter(school=school).count() +
                     ClassRoom.objects.filter(school=school).count() +
                     Student.objects.filter(school=school).count())
        if remaining == 0:
            school.delete()
            print('Deleted School: Smoke School')

    if user:
        user.delete()
        print('Deleted user: smoke_head')

if __name__ == '__main__':
    cleanup()
