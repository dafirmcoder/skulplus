from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0040_alter_competencycomment_education_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="gradescale",
            name="points",
            field=models.IntegerField(default=0),
        ),
    ]

