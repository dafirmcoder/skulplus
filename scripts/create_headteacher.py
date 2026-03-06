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
u = User.objects.filter(username='skulplus').first()
s = School.objects.first()
print('found user', bool(u))
print('found school', bool(s))
if s is None:
    try:
        s = School.objects.create(name='Default School')
        print('created default school')
    except Exception as e:
        print('failed to create default school:', e)
if not u:
    print('User "skulplus" not found; aborting HeadTeacher creation')
else:
    try:
        ht, created = HeadTeacher.objects.get_or_create(user=u, defaults={'school': s})
        print('HeadTeacher created' if created else 'HeadTeacher existed')
    except Exception as e:
        print('failed to create/get HeadTeacher:', e)
