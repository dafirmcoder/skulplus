from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_staff_employment_fields_and_payroll_deductions'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
