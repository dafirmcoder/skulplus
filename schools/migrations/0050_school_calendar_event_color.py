from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0049_school_calendar_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolcalendarevent',
            name='color',
            field=models.CharField(default='#f59e0b', max_length=7),
        ),
    ]

