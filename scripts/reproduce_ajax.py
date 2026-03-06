import os
import sys
import pathlib
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from schools import views
from schools.models import HeadTeacher

rf = RequestFactory()
User = get_user_model()

cases = [
    # (username, class_id, subject_id)
    ('SKULPLUS', '4', '3'),  # SKUL PLUS: class_id=4, subject_id=3
    ('kimani@gmail.com', '5', '1'),  # karuri primary: class_id=5, subject_id=1
]

for username, class_id, subject_id in cases:
    print('\n=== Testing', username, 'class_id=', class_id, 'subject_id=', subject_id, '===')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print('User not found:', username)
        continue
    # ensure user has headteacher attr
    if not hasattr(user, 'headteacher'):
        print('User is not headteacher:', username)
        # try to find a headteacher for the same school
        h = HeadTeacher.objects.filter(user=user).first()
    
    req = rf.get(f'/load-students-for-subject/?class_id={class_id}&subject_id={subject_id}')
    req.user = user
    resp = views.load_students_for_subject(req)
    try:
        content = resp.content.decode('utf-8')
    except Exception:
        content = str(resp)
    print('Status:', getattr(resp, 'status_code', 'n/a'))
    print('Content:', content)
