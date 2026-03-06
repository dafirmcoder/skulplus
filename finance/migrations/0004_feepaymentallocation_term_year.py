from django.db import migrations, models


def backfill_allocation_period(apps, schema_editor):
    FeePaymentAllocation = apps.get_model('finance', 'FeePaymentAllocation')
    for allocation in FeePaymentAllocation.objects.select_related('fee_payment').all():
        payment = allocation.fee_payment
        allocation.allocation_term = payment.term
        allocation.allocation_year = payment.year
        allocation.save(update_fields=['allocation_term', 'allocation_year'])


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_feepaymentallocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='feepaymentallocation',
            name='allocation_term',
            field=models.CharField(default='Term 1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feepaymentallocation',
            name='allocation_year',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
        migrations.RunPython(backfill_allocation_period, migrations.RunPython.noop),
    ]
