import os
import django
import json
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from schools.models import School, HeadTeacher, ClassRoom

User = get_user_model()

email = 'smoke_head@local'
password = 'Sm0keTest!'

# create or get user
user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': 'Smoke', 'last_name': 'Head'})
if created:
    user.set_password(password)
    user.save()

# create or get school
school, _ = School.objects.get_or_create(name='Smoke School', defaults={'school_type': 'Primary', 'address': '', 'phone': '', 'email': ''})

# create headteacher profile
ht, _ = HeadTeacher.objects.get_or_create(user=user, defaults={'school': school, 'full_name': 'Smoke Head', 'phone': ''})

client = Client()
logged_in = client.login(username=email, password=password)
print('logged_in=', logged_in)

results = {}

# Create class
payload = {'name': 'SmokeTestClass', 'section': 'X'}
resp = client.post('/school/headteacher/classes/', data=json.dumps(payload), content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest', HTTP_HOST='127.0.0.1')
results['create_status'] = resp.status_code
try:
    results['create_json'] = resp.json()
except Exception:
    results['create_text'] = resp.content.decode('utf-8', errors='replace')

# Get created id
created_id = None
if resp.status_code == 200:
    try:
        created_id = resp.json().get('class', {}).get('id')
    except Exception:
        pass

# Export excel
resp_x = client.get('/school/headteacher/classes/export/excel/', HTTP_HOST='127.0.0.1')
results['excel_status'] = resp_x.status_code
if resp_x.status_code == 200:
    with open('classes_smoke.xlsx', 'wb') as f:
        f.write(resp_x.content)
    results['excel_saved'] = 'classes_smoke.xlsx'

# Export pdf
resp_p = client.get('/school/headteacher/classes/export/pdf/', HTTP_HOST='127.0.0.1')
results['pdf_status'] = resp_p.status_code
if resp_p.status_code == 200:
    with open('classes_smoke.pdf', 'wb') as f:
        f.write(resp_p.content)
    results['pdf_saved'] = 'classes_smoke.pdf'

# Delete created class
if created_id:
    resp_del = client.post(f'/school/headteacher/classes/delete/{created_id}/', HTTP_HOST='127.0.0.1')
    results['delete_status'] = resp_del.status_code
    try:
        results['delete_json'] = resp_del.json()
    except Exception:
        results['delete_text'] = resp_del.content.decode('utf-8', errors='replace')
else:
    results['delete_status'] = 'no_id'

print(json.dumps(results, indent=2))
