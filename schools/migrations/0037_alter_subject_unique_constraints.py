from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0036_create_lower_upper_primary_levels'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subject',
            name='unique_subject_code_per_school',
        ),
        migrations.RemoveConstraint(
            model_name='subject',
            name='unique_subject_name_per_school',
        ),
        migrations.AddConstraint(
            model_name='subject',
            constraint=models.UniqueConstraint(fields=['school', 'code', 'education_level'], name='unique_subject_code_per_school'),
        ),
        migrations.AddConstraint(
            model_name='subject',
            constraint=models.UniqueConstraint(fields=['school', 'name', 'education_level'], name='unique_subject_name_per_school'),
        ),
    ]
