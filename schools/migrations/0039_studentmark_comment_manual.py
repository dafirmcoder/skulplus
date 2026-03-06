from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0038_cbc_primary_grading'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmark',
            name='comment_manual',
            field=models.BooleanField(default=False),
        ),
    ]