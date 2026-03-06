from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_payrollotherdeduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollAllowance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payroll_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowances_rows', to='payroll.payrollrecord')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
