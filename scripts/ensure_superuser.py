import os
import sys
from pathlib import Path
import django

# Ensure project root is on PYTHONPATH so `config` can be imported
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'adminskulplus')
email = os.environ.get('ADMIN_EMAIL', 'admin@skulplus.up.railway.app')
password = os.environ.get('ADMIN_PASSWORD', '@skulplusadmin')

user = User.objects.filter(username=username).first()
if user is None:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}'")
else:
    changed = False
    if not user.is_superuser or not user.is_staff:
        user.is_superuser = True
        user.is_staff = True
        changed = True
    if email and user.email != email:
        user.email = email
        changed = True
    user.set_password(password)
    changed = True
    if changed:
        user.save()
    print(f"Updated existing superuser '{username}'")
