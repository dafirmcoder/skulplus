from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0053_learning_resources'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted')], default='DRAFT', max_length=12)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_registers', to='schools.classroom')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_created', to='auth.user')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_registers', to='schools.school')),
                ('stream', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_registers', to='schools.stream')),
            ],
            options={
                'ordering': ['-date', '-id'],
                'unique_together': {('school', 'classroom', 'stream', 'date')},
            },
        ),
        migrations.CreateModel(
            name='AttendanceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent'), ('LATE', 'Late'), ('EXCUSED', 'Excused')], default='PRESENT', max_length=12)),
                ('remarks', models.TextField(blank=True, default='')),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='schools.attendanceregister')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_entries', to='schools.student')),
            ],
            options={
                'unique_together': {('register', 'student')},
            },
        ),
    ]
