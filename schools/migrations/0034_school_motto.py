from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0033_competency_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='motto',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
