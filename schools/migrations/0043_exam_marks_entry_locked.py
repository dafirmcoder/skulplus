from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0042_subject_subject_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='marks_entry_locked',
            field=models.BooleanField(default=False),
        ),
    ]
