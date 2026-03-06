import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='staff',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='staff',
            name='employee_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='staff',
            name='employment_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='staff',
            name='employment_type',
            field=models.CharField(choices=[('PERMANENT', 'Permanent'), ('CONTRACT', 'Contract'), ('PART_TIME', 'Part Time'), ('CASUAL', 'Casual')], default='PERMANENT', max_length=20),
        ),
        migrations.AddField(
            model_name='staff',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='kra_pin',
            field=models.CharField(default='PENDING', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='national_id',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='staff',
            name='nhif_number',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='staff',
            name='nssf_number',
            field=models.CharField(default='PENDING', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='phone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='housing_levy_deduction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='nhif_deduction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='nssf_deduction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payrollrecord',
            name='paye_deduction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
