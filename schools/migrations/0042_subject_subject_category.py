from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0041_gradescale_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_category',
            field=models.CharField(
                blank=True,
                choices=[
                    ('STEM', 'STEM'),
                    ('SOCIAL_SCIENCES', 'Social Sciences'),
                    ('ARTS_SPORTS_SCIENCE', 'Arts & Sports Science'),
                ],
                default='',
                max_length=30,
            ),
        ),
    ]
