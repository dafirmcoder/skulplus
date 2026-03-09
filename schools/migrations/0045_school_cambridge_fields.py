from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0044_schooluseraccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='cambridge_grading_system',
            field=models.CharField(
                choices=[('CAMB_9_1', 'Cambridge 9-1'), ('CAMB_A_G', 'Cambridge A-G')],
                default='CAMB_9_1',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='school',
            name='cambridge_show_ranking',
            field=models.BooleanField(default=False),
        ),
    ]
