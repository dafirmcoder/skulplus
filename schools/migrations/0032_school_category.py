from django.db import migrations, models


def set_school_category(apps, schema_editor):
    School = apps.get_model('schools', 'School')
    ClassRoom = apps.get_model('schools', 'ClassRoom')

    for school in School.objects.all():
        levels = ClassRoom.objects.filter(school=school, level__isnull=False).values_list('level__name', flat=True).distinct()
        level_set = {name for name in levels if name}
        if 'Senior' in level_set:
            category = 'SENIOR'
        elif 'Junior' in level_set and 'Primary' in level_set:
            category = 'COMPREHENSIVE'
        elif 'Junior' in level_set:
            category = 'JUNIOR'
        elif 'Primary' in level_set:
            category = 'PRIMARY'
        else:
            category = 'PRIMARY'
        school.school_category = category
        school.save(update_fields=['school_category'])


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0031_subject_related_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='school_category',
            field=models.CharField(choices=[('PRIMARY', 'Primary (Grades 1–6)'), ('JUNIOR', 'Junior (Grades 7–9)'), ('SENIOR', 'Senior (Grades 10–12)'), ('COMPREHENSIVE', 'Comprehensive (Primary + Junior)')], default='PRIMARY', max_length=20),
        ),
        migrations.RunPython(set_school_category, migrations.RunPython.noop),
    ]
