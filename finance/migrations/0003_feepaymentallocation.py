from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_feestructure_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeePaymentAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_head', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fee_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='finance.feepayment')),
            ],
            options={
                'ordering': ['vote_head', 'id'],
            },
        ),
    ]
