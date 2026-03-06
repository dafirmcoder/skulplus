from django.db import migrations, models
import django.db.models.deletion


def set_termdate_school(apps, schema_editor):
    TermDate = apps.get_model('schools', 'TermDate')
    School = apps.get_model('schools', 'School')
    first_school = School.objects.first()
    if first_school:
        TermDate.objects.all().update(school_id=first_school.id)


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0021_alter_termdate_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='termdate',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='term_dates', to='schools.school'),
        ),
        migrations.RunPython(set_termdate_school, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='termdate',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='term_dates', to='schools.school'),
        ),
        migrations.AlterUniqueTogether(
            name='termdate',
            unique_together={('school', 'year', 'term')},
        ),
    ]
