from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0043_exam_marks_entry_locked'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolUserAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('DEAN', 'Dean'), ('SECRETARY', 'Secretary'), ('ACCOUNTS', 'Accounts (Bursar)'), ('DEPUTY', 'Deputy')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('granted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='granted_school_roles', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_access_roles', to='schools.school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_access_role', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'School User Access Role',
                'verbose_name_plural': 'School User Access Roles',
            },
        ),
    ]
