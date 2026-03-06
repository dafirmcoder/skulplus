import os
import sys
# Ensure project root is on sys.path so `config` can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from schools.models import School, HeadTeacher

User = get_user_model()
username = 'SKULPLUS'
password = 'SAMSON123'

u, u_created = User.objects.get_or_create(username=username)
if u_created:
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('user_created')
else:
    print('user_exists')

s, s_created = School.objects.get_or_create(name='SKULPLUS')
print('school_created' if s_created else 'school_exists')

ht, ht_created = HeadTeacher.objects.get_or_create(user=u, defaults={'school': s})
print('headteacher_created' if ht_created else 'headteacher_exists')
