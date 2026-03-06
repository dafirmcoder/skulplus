from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0005_expenditure"),
    ]

    operations = [
        migrations.AddField(
            model_name="expenditure",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("Cash", "Cash"),
                    ("Bank Transfer", "Bank Transfer"),
                    ("M-Pesa", "M-Pesa"),
                ],
                default="Cash",
                max_length=50,
            ),
        ),
    ]
