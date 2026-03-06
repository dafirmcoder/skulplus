from django.db import migrations, models


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('schools', '0010_backfill_subject_codes_and_make_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='allocations', to='schools.subject')),
                ('student', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='subject_allocations', to='schools.student')),
            ],
            options={
                'unique_together': {('subject', 'student')},
            },
        ),
    ]
