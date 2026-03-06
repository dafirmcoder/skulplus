import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='testadmin').exists():
    print('exists')
else:
    User.objects.create_superuser('testadmin','testadmin@example.com','testpass')
    print('created')
