import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from schools.models import School, HeadTeacher, ClassRoom, Student, Subject, SubjectAllocation

User = get_user_model()

def ensure_headteacher():
    user, created = User.objects.get_or_create(username='smoke_head')
    if created:
        user.set_password('smoke_pass')
        user.save()

    school, _ = School.objects.get_or_create(name='Smoke School', defaults={'school_type':'CBE'})
    if not hasattr(user, 'headteacher'):
        HeadTeacher.objects.get_or_create(user=user, school=school, defaults={'full_name':'Smoke Head'})
    return user, school

def setup_data(school):
    cls, _ = ClassRoom.objects.get_or_create(school=school, name='SmokeClass', section='A')
    subj, _ = Subject.objects.get_or_create(school=school, code='S1', name='SmokeSubject')

    # create two students
    s1, _ = Student.objects.get_or_create(school=school, admission_number='S001', first_name='Alice', last_name='One', defaults={'classroom':cls, 'date_of_birth':'2010-01-01', 'gender':'Female', 'admission_date':'2020-01-01'})
    s2, _ = Student.objects.get_or_create(school=school, admission_number='S002', first_name='Bob', last_name='Two', defaults={'classroom':cls, 'date_of_birth':'2010-01-01', 'gender':'Male', 'admission_date':'2020-01-01'})

    # allocate only s1
    SubjectAllocation.objects.get_or_create(subject=subj, student=s1, defaults={'classroom':cls, 'admission_number':s1.admission_number, 'student_name':f"{s1.first_name} {s1.last_name}"})
    return cls, subj, s1, s2

def run_test():
    user, school = ensure_headteacher()
    cls, subj, s1, s2 = setup_data(school)

    client = Client()
    logged = client.login(username=user.username, password='smoke_pass')
    if not logged:
        # try to set session using force_login
        client.force_login(user)

    class_url = f'/school/load-students-for-subject/?class_id={cls.id}'
    subj_url = f'/school/load-students-for-subject/?class_id={cls.id}&subject_id={subj.id}'

    print('GET class-only:', class_url)
    r1 = client.get(class_url, HTTP_HOST='127.0.0.1')
    print('status', r1.status_code, r1.headers.get('Content-Type'))
    print(r1.content.decode())

    print('\nGET class+subject:', subj_url)
    r2 = client.get(subj_url, HTTP_HOST='127.0.0.1')
    print('status', r2.status_code, r2.headers.get('Content-Type'))
    print(r2.content.decode())

if __name__ == '__main__':
    run_test()
