from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_feepaymentallocation_term_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('item', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('vote_head', models.CharField(default='General', max_length=120)),
                ('receipt_invoice_no', models.CharField(blank=True, max_length=120)),
                ('evidence_document', models.FileField(blank=True, null=True, upload_to='expenditures/evidence/')),
                ('source', models.CharField(choices=[('MANUAL', 'Manual'), ('PAYROLL', 'Payroll')], default='MANUAL', max_length=20)),
                ('payroll_month', models.CharField(blank=True, default='', max_length=20)),
                ('payroll_year', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenditures', to='schools.school')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
    ]
