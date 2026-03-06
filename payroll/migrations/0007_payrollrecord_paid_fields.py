from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_payrollrecord_days_worked'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollrecord',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
