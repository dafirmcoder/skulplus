from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0051_competency_comments_and_levels'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='student_limit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='SchoolTypePricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_type', models.CharField(choices=[('CAMBRIDGE', 'Cambridge'), ('CBE', 'CBE')], max_length=20, unique=True)),
                ('price_per_student', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]

