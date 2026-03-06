import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from django.test import Client
c=Client(enforce_csrf_checks=True)
r=c.get('/login/')
print('GET /login/ status', r.status_code)
csr = c.cookies.get('csrftoken')
print('csrftoken cookie present?', bool(csr))
if csr:
    print('csrftoken value (first 8 chars):', csr.value[:8])
# Now POST with the csrf token
data={'csrfmiddlewaretoken': csr.value if csr else '', 'form_type':'login', 'username':'nobody@example.com', 'password':'badpass'}
resp=c.post('/login/', data, follow=True)
print('POST /login/ status', resp.status_code)
print('redirect_chain:', resp.redirect_chain)
print('final path:', resp.request.get('PATH_INFO'))
print('contains login form?', 'name="form_type"' in resp.content.decode('utf-8', errors='ignore'))
