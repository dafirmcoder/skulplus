"""
Example external HTTP script that logs in and posts an exam JSON to the running dev server,
handling CSRF cookies correctly. Adjust `BASE_URL`, `USERNAME`, and `PASSWORD` as needed.

Usage:
  python scripts/post_exam_external.py

This expects your dev server to be running and reachable at BASE_URL.
"""
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://127.0.0.1:8000"  # change if your devserver uses a different host/port
LOGIN_PATH = "/login/"
EXAMS_PATH = "/school/exams/"

USERNAME = "testadmin"
PASSWORD = "testpass"

session = requests.Session()

# 1) GET the login page to obtain CSRF cookie and (optionally) hidden csrf token in form
login_url = BASE_URL + LOGIN_PATH
print(f"GET {login_url}")
resp = session.get(login_url)
resp.raise_for_status()

# The CSRF token is provided as a cookie by Django (usually 'csrftoken').
# Some setups also embed a hidden input named 'csrfmiddlewaretoken' in the form.
csrftoken = session.cookies.get('csrftoken') or session.cookies.get('csrf')
print('CSRF cookie:', csrftoken)

# Try to parse a hidden csrf token from the login form (robustness)
soup = BeautifulSoup(resp.text, 'html.parser')
hidden = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
csrf_form_token = hidden['value'] if hidden else None
if csrf_form_token:
    print('Found form csrf token')

# 2) POST credentials to login. Include csrf from cookie or form as required.
login_data = {
    'username': USERNAME,
    'password': PASSWORD,
}
# include token in form body if present
if csrf_form_token:
    login_data['csrfmiddlewaretoken'] = csrf_form_token

headers = {
    'Referer': login_url,
}
# If cookie exists, requests.Session will send it automatically.
print('POSTing login...')
resp2 = session.post(login_url, data=login_data, headers=headers)
print('Login response status:', resp2.status_code)

# Ensure we're logged in by accessing a protected page
test_url = BASE_URL + '/school/headteacher/dashboard/'
print('Checking dashboard access:', test_url)
test = session.get(test_url)
if test.status_code == 200:
    print('Logged in successfully (accessed dashboard)')
else:
    print('Dashboard access status:', test.status_code)

# 3) GET exams page to ensure CSRF cookie is set for AJAX POST
exams_page = session.get(BASE_URL + EXAMS_PATH)
ex_csrf = session.cookies.get('csrftoken') or session.cookies.get('csrf')
print('Exam page CSRF cookie after GET:', ex_csrf)

# 4) POST exam JSON with X-CSRFToken header
payload = {
    'title': 'External Script Exam',
    'year': 2026,
    'term': 'Term 1',
    'start_date': '2026-06-01',
    'end_date': '2026-06-05',
}
headers = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}
# prefer header token, but include cookie automatically via session
if ex_csrf:
    headers['X-CSRFToken'] = ex_csrf

print('POSTing exam JSON to', BASE_URL + EXAMS_PATH)
resp3 = session.post(BASE_URL + EXAMS_PATH, data=json.dumps(payload), headers=headers)
print('POST status:', resp3.status_code)
try:
    print('Response JSON:', resp3.json())
except Exception:
    print('Response text:', resp3.text)

print('Done')
