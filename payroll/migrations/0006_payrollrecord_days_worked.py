from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_payrollallowance'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollrecord',
            name='days_worked',
            field=models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(30)]),
        ),
    ]
